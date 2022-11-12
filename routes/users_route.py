from fastapi import APIRouter, Depends
from db.models import Token, User
from db import database
# from db.schemas import CreateUser
from uuid import uuid4
from db.crud import create_user_db, get_user_by_token
from db.schemas import CreateUser, UserLogin


database.db.connect()
database.db.create_tables([User, Token])
database.db.close()

sleep_time = 10

async def reset_db_state():
    database.db._state._state.set(database.db_state_default.copy())
    database.db._state.reset()

def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()



user_router = APIRouter()

@user_router.get(path='/users')
def get_users(page: int = 1, per_page: int = 6):
    """Barcha `User` larni olish"""
    users = User.select()
    total_pages = len(users)//per_page
    if total_pages==0:
        total_pages = 1
    page_users = users.paginate(page, per_page)
    data = []
    for user in page_users:
        data.append({
            'id': user.id,
            'email': user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "createdAt": user.createdAt,
            # "avatar": "https://reqres.in/img/faces/1-image.jpg",
        })

    contents = {
        "page": page,
        "per_page": per_page,
        "total": len(users),
        "total_pages": total_pages,
        "data": data,
    }
    return contents

# @user_router.post(path='/')
# def create_user(user: CreateUser):
#     """`User` yaratish"""
#     user_ = User.create(first_name = user.name)

#     contents = {
#         "id": user_.id,
#         "name": user_.name,
#         "createdAt": user_.createdAt,
#     }

#     return contents

@user_router.get(path='/user/{id: int}')
def get_user(id: int = None):
    """`id` ga tegishli `User` ni olish"""
    user = User.get_or_none(id=id)

    if id and user:
        contents = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "createdAt": user.createdAt,
            # "avatar": "https://reqres.in/img/faces/1-image.jpg",
        }
    else:
        contents = {}

    return contents


@user_router.get(path='/user')
def get_current_user(token: str):
    """Hozirgi `User` ni olish"""
    user = get_user_by_token(token=token)

    if user is not None:
        email = user.email
        first_name = user.first_name
        last_name = user.last_name
        createdAt = user.createdAt
    else:
        contents = {'error': 'invalid token'}
        return contents

    contents = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'createdAt': createdAt,
    }

    return contents


@user_router.put(path='/register')
def create_user(user: CreateUser):
    """`User` yaratish"""
    token = create_user_db(user)

    if token is not None:
        return token.token
    return None

@user_router.post('/login')
def user_login(user_login: UserLogin):
    """`User` ni login qilish"""
    pass


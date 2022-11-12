from sqlite3 import IntegrityError
from typing import Any
from db.models import User, Token
from db.schemas import CreateUser


def get_user_by_token(token):
    token_ = Token.get_or_none(token=token)
    if token_ is not None:
        user = token_.user
    else:
        user = None
    return user


def create_user_db(user: CreateUser) -> Any | None:
    try:
        user_ = User.create(
            email = user.email,
            first_name = user.first_name,
            last_name = user.last_name,
            password = user.password,
        )
    except IntegrityError as e:
        return {'error': f'{e}'}


    token_ = Token.create(user = user_)

    return token_


#
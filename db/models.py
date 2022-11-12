import peewee as pw
from uuid import uuid4
from .database import db
from datetime import datetime


class BaseModel(pw.Model):
    """Asos model"""
    class Meta:
        database = db


class User(BaseModel):
    "User modeli"
    email = pw.CharField(unique=True, index=True)
    first_name = pw.CharField()
    last_name = pw.CharField(null=True)
    password = pw.CharField(null=True)
    image = pw.CharField(unique=True, null=True)
    createdAt = pw.DateTimeField(default=datetime.now)


class Token(BaseModel):
    """Token"""
    user = pw.ForeignKeyField(User, on_delete='CASCADE', backref='token')
    token = pw.UUIDField(unique=True, default=uuid4)

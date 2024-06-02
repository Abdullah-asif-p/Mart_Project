from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, text
from uuid import UUID, uuid4
from .db import db_dependency


# Data to save in the database
class Users(SQLModel, table=True):
    user_id: str = Field(primary_key=True, default_factory=uuid4)
    username: str = Field()
    role: str = Field(default="User")
    email: Optional[str] = Field(default=None)
    hashed_password: str = Field()


class SuperAdmin(SQLModel):
    username: str = Field()
    password: str = Field()


class Token(SQLModel):
    access_token: str
    token_type: str


# User input
class UserCreate(SQLModel):
    username: str
    email: str
    password: str

class AuthUser(SQLModel):
    username:str
    password:str

class ChangeUsername(SQLModel):
    new_username: str

class ChangePassword(SQLModel):
    new_password :str


class ChangeEmail(SQLModel):
    email: str


class CurrentUser(SQLModel):
    user_id: str 
    username: str
    email: Optional[str]

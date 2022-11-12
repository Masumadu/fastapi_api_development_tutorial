from pydantic import BaseModel, EmailStr
import datetime
from typing import Optional

from pydantic.types import conint


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str]


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    id: int
    created:  datetime.datetime

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created:  datetime.datetime
    owner_id: int
    owner: User

    class Config:
        orm_mode = True


class PostVote(BaseModel):
    Post: Post
    votes: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

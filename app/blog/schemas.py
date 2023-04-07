from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, root_validator


class UserSignUpBody(BaseModel):  # DTO/Schema
    name: str
    email: EmailStr
    password: str
    confirm_password: str

    @root_validator
    def check_passwords_match(cls, values):
        pw1, pw2 = values.get("password"), values.get("confirm_password")
        if pw1 != pw2:
            raise ValueError("passwords do not match")
        return values


class UserSignUpResponse(BaseModel):
    email: str
    name: str
    id: int
    create_at: datetime


class LoginBody(BaseModel):  # DTO/Schema
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    token: str


class CreateListBody(BaseModel):
    name: str
    description: str


class CreateListResponse(CreateListBody):
    id: int
    owner_id: int
    create_at: datetime


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []

    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

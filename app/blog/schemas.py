from datetime import datetime
from enum import Enum
from typing import Annotated, List, Optional, Union

from pydantic import BaseModel, EmailStr, Field, root_validator
from pydantic.schema import Dict, Optional


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
    email: EmailStr
    name: str
    id: int
    created_at: datetime


class LoginBody(BaseModel):  # DTO/Schema
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    token: str = Field(
        default="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2ODExODI0MDd9.j7bP8zGtdy_GHm4zb_nN_nUy_kcGiyQZ_JFO7QTwSlQ"
    )


class CreateListBody(BaseModel):
    name: str
    description: str


class CreateListResponse(CreateListBody):
    id: int
    owner_id: int
    created_at: datetime


class GetListByIdResponse(BaseModel):
    id: int
    description: str
    name: str
    created_at: datetime

    class Config:
        orm_mode = True


class TodoStatus(str, Enum):
    todo = "Unfinished"
    finished = "Finished"


class CreateTodoBody(BaseModel):
    list_id: int
    title: str = Field(default="None", title="The description of the item", max_length=300)
    description: str
    due_date: datetime


class CreateTodoResponse(BaseModel):
    list_id: int
    title: str = Field(default="None")
    description: str
    due_date: datetime
    id: int
    status: TodoStatus
    finished_at: Optional[datetime] = Field(default=None, example=None)
    created_at: datetime


class UpdateTodoBody(BaseModel):
    todo_id: int
    status: TodoStatus


class UpdateTodoResponse(BaseModel):
    list_id: int
    title: str = Field(default="None")
    description: str
    due_date: datetime
    id: int
    status: TodoStatus
    finished_at: Optional[datetime] = Field(default=None, example=None)
    created_at: datetime


class Todo(BaseModel):
    list_id: int
    title: str = Field(default="None")
    description: str
    due_date: datetime
    id: int
    status: TodoStatus
    finished_at: Optional[datetime] = Field(default=None, example=None)
    created_at: datetime

    class Config:
        orm_mode = True


class GetTodoStatus(str, Enum):
    default = "All"
    finished = "Finished"
    unfinished = "Unfinished"


# ......................................... #
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

from fastapi import HTTPException, Response, status
from fastapi_pagination import LimitOffsetPage, Page, add_pagination, paginate
from sqlalchemy.orm import Session

from .. import models, schemas
from ..services import todo_service


def create(list_id, title, description, due_date, owner_id, db: Session):
    todo = todo_service.create_todo(
        list_id, title, description, due_date, owner_id, db)
    return todo


def get_todo(user_id, list_id, status, db: Session):
    todo = todo_service.get_todo(user_id, list_id, status, db)
    return paginate(todo)


def delete(user_id, todo_id, db: Session):
    todo = todo_service.delete_todo(user_id, todo_id, db)
    return todo


def update(todo_id, status, user_id, db: Session):
    todo = todo_service.update_todo(todo_id, status, user_id, db)
    return todo

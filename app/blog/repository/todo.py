from fastapi import HTTPException, Response, status
from fastapi_pagination import LimitOffsetPage, Page, add_pagination, paginate
from sqlalchemy.orm import Session

from .. import models, schemas
from ..services import todo_service


def create(data: schemas.CreateTodoResponse, owner_id, response: Response, db: Session):
    list_id = data.list_id
    title = data.title
    description = data.description
    due_date = data.due_date
    todo = todo_service.create_todo(list_id, title, description, due_date, owner_id, db)
    return todo.__dict__


def get_todo(user_id, list_id, status, db: Session):
    todo = todo_service.get_todo(user_id, list_id, status, db)
    return paginate(todo)


def delete(user_id, id, db: Session):
    todo = todo_service.delete_todo(user_id, id, db)
    return todo


def update(data: schemas.UpdateTodoBody, user_id, db: Session):
    todo_id = data.todo_id
    status = data.status
    todo = todo_service.update_todo(todo_id, status, user_id, db)
    return todo.__dict__

from datetime import datetime, timezone

from fastapi_pagination import LimitOffsetPage, Page, add_pagination, paginate
from sqlalchemy.orm import Session

from ... import errors
from .. import models, schemas, token
from ..hashing import Hash
import pytz


def create_list(owner_id, name, description, db: Session):
    list_todo = db.query(models.ToDoList).filter(
        models.ToDoList.name == name).first()
    if list_todo:
        raise errors.Used()
    utc_now = datetime.utcnow()
    created_at = utc_now
    new_list = models.ToDoList(
        name=name, description=description, created_at=created_at, owner_id=owner_id)
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return dict(name=name, description=description, created_at=created_at, owner_id=owner_id)


def get_list_id(user_id, list_id, db: Session):
    list_todo = db.query(models.ToDoList).filter(
        models.ToDoList.id == list_id).first()
    if not list_todo:
        raise errors.NotFound()
    # neu user_id khac list's owner_id
    if user_id != list_todo.owner_id:
        raise errors.NotFound()
    return dict(id=list_todo.id, description=list_todo.description, name=list_todo.name, created_at=list_todo.created_at, owner_id=list_todo.owner_id)


def get_list(user_id, db: Session):
    list_todo = db.query(models.ToDoList).filter(
        models.ToDoList.owner_id == user_id).all()
    return list_todo


def delete_list(user_id, list_id, db: Session):
    list_todo = db.query(models.ToDoList).filter(
        models.ToDoList.id == list_id).first()
    if not list_todo:
        raise errors.NotFound()
    # neu user_id khac list's owner_id
    if user_id != list_todo.owner_id:
        raise errors.NotFound()
    todo_delete = db.query(models.ToDo).filter(
        models.ToDo.list_id == list_id).delete()
    list_delete = db.query(models.ToDoList).filter(
        models.ToDoList.id == list_id)
    # list.todos = []
    list_delete.delete(synchronize_session=False)
    db.commit()

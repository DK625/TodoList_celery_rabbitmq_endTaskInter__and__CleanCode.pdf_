from datetime import datetime, timezone

from fastapi_pagination import LimitOffsetPage, Page, add_pagination, paginate
from sqlalchemy.orm import Session

from ... import errors
from .. import models, schemas, token
from ..hashing import Hash
import pytz

local_tz = pytz.timezone("Asia/Ho_Chi_Minh")


def create_list(owner_id, name, description, db: Session):
    list_todo = db.query(models.ToDoList).filter(models.ToDoList.name == name).first()
    if list_todo:
        raise errors.Used()
    user = db.query(models.User).filter(models.User.id == owner_id).first()
    # truyen user_id khong ton tai
    if not user:
        raise errors.NotFound()
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    local_now = utc_now.astimezone(local_tz)
    created_at = local_now.isoformat()
    new_list = models.ToDoList(name=name, description=description, created_at=created_at, owner_id=owner_id)
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return new_list


def get_list_id(user_id, id, db: Session):
    list_todo = db.query(models.ToDoList).filter(models.ToDoList.id == id).first()
    if not list_todo:
        raise errors.NotFound()
    # neu user_id khac list's owner_id
    if user_id != list_todo.owner_id:
        raise errors.NotFound()
    return list_todo


def get_list(user_id, db: Session):
    list_todo = db.query(models.ToDoList).filter(models.ToDoList.owner_id == user_id).all()
    return list_todo


def delete_list(user_id, id, db: Session):
    list_todo = db.query(models.ToDoList).filter(models.ToDoList.id == id).first()
    if not list_todo:
        raise errors.NotFound()
    # neu user_id khac list's owner_id
    if user_id != list_todo.owner_id:
        raise errors.NotFound()
    todo_delete = db.query(models.ToDo).filter(models.ToDo.list_id == id).delete()
    list_delete = db.query(models.ToDoList).filter(models.ToDoList.id == id)
    # list.todos = []
    list_delete.delete(synchronize_session=False)
    db.commit()
    return "done"

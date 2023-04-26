from datetime import datetime

from fastapi_pagination import LimitOffsetPage, Page, add_pagination, paginate
from sqlalchemy.orm import Session

from ... import errors
from .. import models, schemas, token
from ..hashing import Hash
from ..celery_tasks.tasks import send_email
import pytz

local_tz = pytz.timezone("Asia/Ho_Chi_Minh")


def create_todo(list_id, title, description, due_date, owner_id, db: Session):
    list_todo = db.query(models.ToDoList).filter(
        models.ToDoList.id == list_id).first()
    if not list_todo:
        raise errors.NotFound()
    # neu user_id khac list's owner_id
    if owner_id != list_todo.owner_id:
        raise errors.NotFound()
    todo = db.query(models.ToDo).filter(models.ToDo.title == title).first()
    if todo:
        raise errors.Used()
    utc_now = datetime.utcnow()
    created_at = utc_now
    new_todo = models.ToDo(
        title=title,
        description=description,
        due_date=due_date,
        list_id=list_id,
        created_at=created_at,
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return dict(
        list_id=new_todo.list_id,
        title=new_todo.title,
        description=new_todo.description,
        due_date=new_todo.due_date,
        id=new_todo.id,
        status=new_todo.status,
        finished_at=new_todo.finished_at,
        created_at=new_todo.created_at,
    )


def update_todo(todo_id, status, user_id, db: Session):
    todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if not todo:
        raise errors.NotFound()
    list_todo = db.query(models.ToDoList).filter(
        models.ToDoList.id == todo.list_id).first()
    finished_at = None
    # neu user_id khac list's owner_id
    if user_id != list_todo.owner_id:
        raise errors.NotFound()
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if status == "Finished":
        utc_now = datetime.utcnow()
        finished_at = utc_now
    else:
        finished_at = None
    message = {"title": todo.title, "description": todo.description,
               "status": status, "receiver": user.email}
    mess = dict(message)
    send_email.delay(mess)
    todos = db.query(models.ToDo).filter(models.ToDo.id == todo_id)
    todos.update({"status": status, "finished_at": finished_at})
    db.commit()
    todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    return dict(
        list_id=todo.list_id,
        title=todo.title,
        description=todo.description,
        due_date=todo.due_date,
        id=todo.id,
        status=todo.status,
        finished_at=todo.finished_at,
        created_at=todo.created_at,
    )


def get_todo(user_id, list_id, status, db: Session):
    list_todo = db.query(models.ToDoList).filter(
        models.ToDoList.id == list_id).first()
    if not list_todo:
        raise errors.NotFound()
    if user_id != list_todo.owner_id:
        raise errors.NotFound()
    if status == "All":
        todo = db.query(models.ToDo).filter(
            models.ToDo.list_id == list_id).all()
        return todo
    todo = db.query(models.ToDo).filter(
        models.ToDo.list_id == list_id, status == status).all()
    return todo


def delete_todo(user_id, todo_id, db: Session):
    todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if not todo:
        raise errors.NotFound()
    list_todo = db.query(models.ToDoList).filter(
        models.ToDoList.id == todo.list_id).first()
    # neu user_id khac list's owner_id
    if user_id != list_todo.owner_id:
        raise errors.NotFound()
    todo_delete = db.query(models.ToDo).filter(models.ToDo.id == todo_id)
    todo_delete.delete(synchronize_session=False)
    db.commit()

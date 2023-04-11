from datetime import datetime, timezone

from fastapi_pagination import LimitOffsetPage, Page, add_pagination, paginate
from sqlalchemy.orm import Session

from ... import errors
from .. import models, schemas, token
from ..hashing import Hash


def create_todo(list_id, title, description, due_date, owner_id, db: Session):
    list = db.query(models.ToDoList).filter(models.ToDoList.id == list_id).first()
    if not list:
        raise errors.NotFound()
    # neu user_id khac list's owner_id
    if owner_id != list.owner_id:
        raise errors.NotFound()
    todo = db.query(models.ToDo).filter(models.ToDo.title == title).first()
    if todo:
        raise errors.Used()
    new_todo = models.ToDo(
        title=title,
        description=description,
        due_date=due_date,
        list_id=list_id,
        created_at=datetime.utcnow().isoformat(),
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


def update_todo(todo_id, status, user_id, db: Session):
    todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if not todo:
        raise errors.NotFound()
    list = db.query(models.ToDoList).filter(models.ToDoList.id == todo.list_id).first()
    finished_at = None
    # neu user_id khac list's owner_id
    if user_id != list.owner_id:
        raise errors.NotFound()
    if status == "Finished":
        finished_at = datetime.utcnow().isoformat()
    else:
        finished_at = None
    todos = db.query(models.ToDo).filter(models.ToDo.id == todo_id)
    todos.update({"status": status, "finished_at": finished_at})
    db.commit()
    todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    return todo


def get_todo(user_id, list_id, status, db: Session):
    list = db.query(models.ToDoList).filter(models.ToDoList.id == list_id).first()
    if not list:
        raise errors.NotFound()
    if user_id != list.owner_id:
        raise errors.NotFound()
    if status == "All":
        todo = db.query(models.ToDo).filter(models.ToDo.list_id == list_id).all()
        return todo
    todo = db.query(models.ToDo).filter(models.ToDo.list_id == list_id, status == status).all()
    return todo


def delete_todo(user_id, id, db: Session):
    todo = db.query(models.ToDo).filter(models.ToDo.id == id).first()
    if not todo:
        raise errors.NotFound()
    list = db.query(models.ToDoList).filter(models.ToDoList.id == todo.list_id).first()
    # neu user_id khac list's owner_id
    if user_id != list.owner_id:
        raise errors.NotFound()
    todo_delete = db.query(models.ToDo).filter(models.ToDo.id == id)
    todo_delete.delete(synchronize_session=False)
    db.commit()
    return "done"

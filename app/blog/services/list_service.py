from datetime import datetime, timezone

from fastapi_pagination import LimitOffsetPage, Page, add_pagination, paginate
from sqlalchemy.orm import Session

from ... import errors
from .. import models, schemas, token
from ..hashing import Hash


def create_list(owner_id, name, description, db: Session):
    list = db.query(models.ToDoList).filter(models.ToDoList.name == name).first()
    if list:
        raise errors.Used()
    user = db.query(models.User).filter(models.User.id == owner_id).first()
    # truyen user_id khong ton tai
    if not user:
        raise errors.NotFound()
    new_list = models.ToDoList(
        name=name, description=description, created_at=datetime.utcnow().isoformat(), owner_id=owner_id
    )
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return new_list


def get_list_id(user_id, id, db: Session):
    list = db.query(models.ToDoList).filter(models.ToDoList.id == id).first()
    if not list:
        raise errors.NotFound()
    # neu user_id khac list's owner_id
    if user_id != list.owner_id:
        raise errors.NotFound()
    return list


def get_list(user_id, db: Session):
    list = db.query(models.ToDoList).filter(models.ToDoList.owner_id == user_id).all()
    return list


def delete_list(user_id, id, db: Session):
    list = db.query(models.ToDoList).filter(models.ToDoList.id == id).first()
    if not list:
        raise errors.NotFound()
    # neu user_id khac list's owner_id
    if user_id != list.owner_id:
        raise errors.NotFound()
    list_delete = db.query(models.ToDoList).filter(models.ToDoList.id == id)
    list_delete.delete(synchronize_session=False)
    db.commit()
    return "done"

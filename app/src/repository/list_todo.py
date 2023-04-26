from fastapi import HTTPException, Response, status
from fastapi_pagination import LimitOffsetPage, Page, add_pagination, paginate
from sqlalchemy.orm import Session

from .. import models, schemas
from ..services import list_service


def create(name, description, owner_id, db: Session):
    list_todo = list_service.create_list(owner_id, name, description, db)
    return list_todo


def get_list_id(user_id, list_id, db: Session):
    list_todo = list_service.get_list_id(user_id, list_id, db)
    return list_todo


def get_list(user_id, db: Session):
    list_todo = list_service.get_list(user_id, db)
    return paginate(list_todo)


def delete(user_id, list_id, db: Session):
    list_todo = list_service.delete_list(user_id, list_id, db)
    return list_todo

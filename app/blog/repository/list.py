from fastapi import HTTPException, Response, status
from fastapi_pagination import LimitOffsetPage, Page, add_pagination, paginate
from sqlalchemy.orm import Session

from .. import models, schemas
from ..services import list_service


def create(data: schemas.UserSignUpBody, owner_id, response: Response, db: Session):
    name = data.name
    description = data.description
    list = list_service.create_list(owner_id, name, description, db)
    return list.__dict__


def get_list_id(user_id, id, response: Response, db: Session):
    list = list_service.get_list_id(user_id, id, db)
    return list.__dict__


def get_list(user_id, response: Response, db: Session):
    list = list_service.get_list(user_id, db)
    return paginate(list)


def delete(user_id, id, db: Session):
    list = list_service.delete_list(user_id, id, db)
    return list

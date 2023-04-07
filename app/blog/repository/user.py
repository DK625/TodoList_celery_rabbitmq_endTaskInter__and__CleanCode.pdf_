from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session

from app.blog import models, schemas

from ..hashing import Hash
from ..services import user_service


def create(data: schemas.UserSignUpBody, response: Response, db: Session):
    name = data.name
    email = data.email
    password = data.password
    user = user_service.handle_user_sign_up(name, email, password, db)
    return user.__dict__


def login(data: schemas.LoginBody, response: Response, db: Session):
    email = data.email
    password = data.password
    user = user_service.handle_user_login(email, password, db)
    return user

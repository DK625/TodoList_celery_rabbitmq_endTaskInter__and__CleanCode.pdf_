from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session

from app.src import models, schemas

from ..hashing import Hash
from ..services import user_service


def create(name, email, password, db: Session):
    user = user_service.handle_user_sign_up(name, email, password, db)
    return dict(
        email=user.email,
        name=user.name,
        id=user.id,
        created_at=user.created_at,
    )


def login(email, password, db: Session):
    user = user_service.handle_user_login(email, password, db)
    return user

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from ... import errors
from .. import models, schemas, token
from ..hashing import Hash


def handle_user_sign_up(name, email, password, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        raise errors.DuplicateUserError()
    new_user = models.User(
        name=name, email=email, password=Hash.bcrypt(password), created_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def handle_user_login(email, password, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise errors.NotFound()
    if not Hash.verify(user.password, password):
        raise errors.IncorrectPasswordError()
    access_token = token.create_access_token(data={"user_id": user.id})
    return {"token": access_token}

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from ... import errors
from .. import models, schemas, token
from ..hashing import Hash


def create_list(owner_id, name, description, db: Session):
    list = db.query(models.ToDoList).filter(models.ToDoList.name == name).first()
    if list:
        raise errors.DuplicateUserError()
    new_list = models.ToDoList(
        name=name, description=description, create_at=datetime.utcnow().isoformat(), owner_id=owner_id
    )
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return new_list

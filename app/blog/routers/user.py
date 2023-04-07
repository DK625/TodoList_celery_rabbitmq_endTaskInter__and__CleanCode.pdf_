from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import database, models, schemas
from ..repository import user

router = APIRouter(
    # prefix="/user",
    tags=["Users"]
)

get_db = database.get_db


@router.get("/{id}", response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.show(id, db)

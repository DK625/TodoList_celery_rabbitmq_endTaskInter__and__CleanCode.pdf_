from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..services import list_service


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(owner_id, data: schemas.UserSignUpBody, response: Response, db: Session):
    name = data.name
    description = data.description
    list = list_service.create_list(owner_id, name, description, db)
    return list.__dict__


def destroy(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")

    blog.delete(synchronize_session=False)
    db.commit()
    return "done"


def update(id: int, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")

    blog.update(request)
    db.commit()
    return "updated"


def show(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
    return blog

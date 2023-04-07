from typing import List

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from ... import errors
from .. import database, models, oauth2, schemas, token
from ..jwt_bearer import JWTBearer
from ..repository import list

router = APIRouter(prefix="/lists", tags=["Lists"])

get_db = database.get_db


@router.post("/", dependencies=[Depends(JWTBearer(Request))], response_model=schemas.CreateListResponse)
def create_new_list(
    request: Request,
    response: Response,
    payload: schemas.CreateListBody,
    db: Session = Depends(get_db),
):
    try:
        key = (request.headers.get("authorization")).split(" ")[-1]
        auth_info = token.verify_token(key)
        print("check: ", auth_info)
        # post_list = list.create(payload, response, db)
        return post_list
    except errors.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Not found!"})
    except errors.IncorrectPasswordError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"error": "Wrong password!"})


# @router.get('/', response_model=List[schemas.ShowBlog])
@router.get("/", dependencies=[Depends(JWTBearer())])
# def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
def all(db: Session = Depends(get_db)):
    return list.get_all(db)


# @router.post("/", status_code=status.HTTP_201_CREATED)
# def create(
#     request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)
# ):
#     return list.create(request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return list.destroy(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(
    id: int,
    request: schemas.Blog,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return list.update(id, request, db)


@router.get("/{id}", status_code=200, response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return list.show(id, db)

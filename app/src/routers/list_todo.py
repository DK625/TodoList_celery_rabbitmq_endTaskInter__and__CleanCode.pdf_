from typing import List

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_pagination import LimitOffsetPage, Page, add_pagination, paginate
from sqlalchemy.orm import Session

from ... import errors
from .. import dependencies, models, schemas, token
from ..jwt_bearer import User, get_user
from ..repository import list_todo

router = APIRouter()

get_db = dependencies.get_db


@router.post("/", response_model=schemas.CreateListResponse)
def create_new_list(
    payload: schemas.CreateListBody,
    db: Session = Depends(get_db),
    user: User = Depends(get_user),
):
    try:
        name = payload.name
        description = payload.description
        post_list = list_todo.create(name, description, user.id, db)
        return post_list
    except errors.Used:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
                            "error": "List's name has been used!"})
    # except errors.NotFound:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
    #                         "error": "List Not Found!"})


@router.get("/{id}", response_model=schemas.GetListByIdResponse)
def get_list_by_id(list_id: str, db: Session = Depends(get_db), user: User = Depends(get_user)):
    try:
        get_list = list_todo.get_list_id(user.id, list_id, db)
        return get_list
    except errors.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "error": "List Not Found!"})


@router.get("/", response_model=Page[schemas.GetListByIdResponse])
def get_list(db: Session = Depends(get_db), user: User = Depends(get_user)):
    get_list = list_todo.get_list(user.id, db)
    return get_list


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_list(list_id: str, db: Session = Depends(get_db), user: User = Depends(get_user)):
    try:
        delete_list = list_todo.delete(user.id, list_id, db)
        return delete_list
    except errors.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "error": "List Not Found!"})

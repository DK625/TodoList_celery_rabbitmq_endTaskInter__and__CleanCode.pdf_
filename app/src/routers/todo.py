from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from ... import errors
from .. import dependencies, models, schemas, token

# from ..jwt_bearer import JWTBearer
from ..repository import todo
from ..jwt_bearer import User, get_user

router = APIRouter()

get_db = dependencies.get_db


@router.post("/", response_model=schemas.CreateTodoResponse)
def create_new_todo(payload: schemas.CreateTodoBody, db: Session = Depends(get_db), user: User = Depends(get_user)):
    try:
        list_id = payload.list_id
        title = payload.title
        description = payload.description
        due_date = payload.due_date
        post_todo = todo.create(
            list_id, title, description, due_date, user.id, db)
        return post_todo
    except errors.Used:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
                            "error": "Todo's title has been used!"})
    except errors.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "error": "List Not Found!"})


@router.get("/", response_model=Page[schemas.Todo])
def get_todo(
    list_id: str, status_todo: schemas.GetTodoStatus, db: Session = Depends(get_db), user: User = Depends(get_user)
):
    try:
        get_todo = todo.get_todo(user.id, list_id, status_todo, db)
        return get_todo
    except errors.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "error": "List Not Found!"})


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: str, db: Session = Depends(get_db), user: User = Depends(get_user)):
    try:
        delete_todo = todo.delete(user.id, todo_id, db)
        return delete_todo
    except errors.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "error": "Todo Not Found!"})


@router.patch(
    "/",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.UpdateTodoResponse,
)
def update_an_exit_todo(
    payload: schemas.UpdateTodoBody, db: Session = Depends(get_db), user: User = Depends(get_user)
):
    try:
        todo_id = payload.todo_id
        status_todo = payload.status
        update_todo = todo.update(todo_id, status_todo, user.id, db)
        return update_todo
    except errors.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "error": "Todo Not Found!"})

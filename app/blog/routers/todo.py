from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from ... import errors
from .. import database, models, oauth2, schemas, token
from ..jwt_bearer import JWTBearer
from ..repository import todo

router = APIRouter(prefix="/todos", tags=["Todo"])

get_db = database.get_db


@router.post("/", dependencies=[Depends(JWTBearer(Request))], response_model=schemas.CreateTodoResponse)
def create_new_todo(
    request: Request, response: Response, payload: schemas.CreateTodoBody, db: Session = Depends(get_db)
):
    try:
        key = (request.headers.get("authorization")).split(" ")[-1]
        auth_info = token.verify_token(key)
        user_id = auth_info["user_id"]
        post_todo = todo.create(payload, user_id, response, db)
        return post_todo
    except errors.Used:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"error": "Information has been used!"})
    except errors.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "List Not Found!"})


@router.get("/", dependencies=[Depends(JWTBearer(Request))], response_model=Page[schemas.Todo])
def get_todo(list_id: int, status: schemas.GetTodoStatus, request: Request, db: Session = Depends(get_db)):
    try:
        key = (request.headers.get("authorization")).split(" ")[-1]
        auth_info = token.verify_token(key)
        user_id = auth_info["user_id"]
        get_todo = todo.get_todo(user_id, list_id, status, db)
        return get_todo
    except errors.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "List Not Found!"})


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(JWTBearer(Request))])
def delete_todo(todo_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        key = (request.headers.get("authorization")).split(" ")[-1]
        auth_info = token.verify_token(key)
        user_id = auth_info["user_id"]
        delete_todo = todo.delete(user_id, todo_id, db)
        return delete_todo
    except errors.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Todo Not Found!"})


@router.patch(
    "/",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(JWTBearer(Request))],
    response_model=schemas.UpdateTodoResponse,
)
def update_an_exit_todo(request: Request, payload: schemas.UpdateTodoBody, db: Session = Depends(get_db)):
    try:
        key = (request.headers.get("authorization")).split(" ")[-1]
        auth_info = token.verify_token(key)
        user_id = auth_info["user_id"]
        update_todo = todo.update(payload, user_id, db)
        return update_todo
    except errors.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Todo Not Found!"})

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ... import errors
from .. import database, models, schemas, token
from ..hashing import Hash
from ..repository import user

router = APIRouter(tags=["Auth Sign Up and Login"])
get_db = database.get_db


@router.post("/sign-up", response_model=schemas.UserSignUpResponse)
def sign_up(request: schemas.UserSignUpBody, response: Response, db: Session = Depends(get_db)):
    try:
        raw_user = user.create(request, response, db)
        return raw_user
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"error": "Your email is already exist!"})


@router.post("/login", response_model=schemas.LoginResponse)
def login(request: schemas.LoginBody, response: Response, db: Session = Depends(get_db)):
    try:
        raw_user = user.login(request, response, db)
        return raw_user
    except errors.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Not found!"})
    except errors.IncorrectPasswordError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"error": "Wrong password!"})

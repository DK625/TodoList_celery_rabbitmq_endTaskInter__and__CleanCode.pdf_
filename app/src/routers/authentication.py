from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ... import errors
from .. import dependencies, models, schemas, token
from ..hashing import Hash
from ..repository import user

router = APIRouter(tags=["Auth Sign Up and Login"])
get_db = dependencies.get_db


@router.post("/sign-up", response_model=schemas.UserSignUpResponse)
def sign_up(request: schemas.UserSignUpBody, db: Session = Depends(get_db)):
    try:
        name = request.name
        email = request.email
        password = request.password
        raw_user = user.create(name, email, password, db)
        return raw_user
    except errors.DuplicateUserError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"error": "Your email is already exist!"})


@router.post("/login", response_model=schemas.LoginResponse)
def login(request: schemas.LoginBody, db: Session = Depends(get_db)):
    try:
        email = request.email
        password = request.password
        raw_user = user.login(email, password, db)
        return raw_user
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Wrong username or password informations"}
        )

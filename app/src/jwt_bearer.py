from typing import Optional

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from . import token as auth_service
from .schemas import User


class AuthHttpBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        try:
            return await super().__call__(request)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail={"error": e.detail})


def get_user(token: HTTPAuthorizationCredentials = Depends(AuthHttpBearer())):
    try:
        payload = auth_service.verify_token(token=token.credentials)
    except auth_service.TokenError:
        raise HTTPException(status_code=401, detail={"error": "Invalid token"})
    return User(id=payload["user_id"])

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.security import HTTPBearer

from . import models
from .database import engine
from .routers import authentication, list, user

app = FastAPI()


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    # return JSONResponse(content={"error": str(exc)})
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(list.router)
app.include_router(user.router)

# uvicorn app.blog.main:app --reload
# {
#   "email": "minhha10c8@gmail.com",
#   "password": "12345"
# }

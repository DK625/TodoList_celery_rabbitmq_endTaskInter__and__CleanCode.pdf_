import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.security import HTTPBearer
from fastapi_pagination import LimitOffsetPage, Page, add_pagination, paginate

from . import models
from .db.session import engine
from .routers import authentication, list_todo, todo

app = FastAPI()


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    # print(exec)
    return JSONResponse(content={"error": str(exc.detail["error"])}, status_code=exc.status_code)


models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(list_todo.router)
app.include_router(todo.router)
add_pagination(app)

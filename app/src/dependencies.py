from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from ..config import settings
from .db.session import Base, SessionLocal, engine


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

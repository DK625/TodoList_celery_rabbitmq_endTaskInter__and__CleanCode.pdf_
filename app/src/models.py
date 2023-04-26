# import datetime
from abc import ABC

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime)
    todo_lists = relationship("ToDoList", backref="owner")


class ToDoList(Base):
    __tablename__ = "lists"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(100))
    created_at = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("users.id"))
    todos = relationship("ToDo", backref="list")


class ToDo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(100))
    due_date = Column(DateTime)
    status = Column(String(100), default="Unfinished")
    finished_at = Column(DateTime)
    list_id = Column(Integer, ForeignKey("lists.id"))
    created_at = Column(DateTime)

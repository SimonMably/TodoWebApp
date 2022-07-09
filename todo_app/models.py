import os
import datetime as dt
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import query, relationship
from todo_app import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    user_tasks = relationship("Task", back_populates="author")
    
    def __repr__(self):
        return f"{self.username}"


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="user_tasks")
    user_task = db.Column(db.String(350), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    published_date = db.Column(db.String(250), nullable=False)
    
    # def __repr__(self):
    #     return f"{self.user_task}"

if not os.path.isfile("todo_db.db"):
    db.create_all()

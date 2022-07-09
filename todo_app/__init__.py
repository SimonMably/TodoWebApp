from datetime import datetime as dt
import os

from dotenv import load_dotenv
import psycopg2 as pc
from flask import Flask
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from sqlalchemy.orm import query
from flask_sqlalchemy import SQLAlchemy


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

app = Flask(__name__)
ckeditor = CKEditor(app)

app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo_db.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/todo_db"
db = SQLAlchemy(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

from todo_app import routes
from datetime import datetime as dt
import imp
import os

from flask import Flask
from flask_ckeditor import CKEditor
from flask_login import LoginManager

app = Flask(__name__)
ckeditor = CKEditor(app)

# Database Stuff


# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

from todo_app import routes
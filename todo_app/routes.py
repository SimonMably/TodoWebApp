from datetime import datetime as dt
from functools import wraps

from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from todo_app import app, login_manager  #, db
# from todo_app.models import Users, Tasks
# from todo_app.forms import RegisterUserForm, LoginUserForm, AddTaskForm


@app.context_processor
def inject_now():
    """"""
    return {"now": dt.now()}


# TODO: Use wraps() from funtools here

@login_manager.user_loader
def load_user(user_id:int):
    """"""
    return  # TODO: Create database, insert request for user id from User table here


@app.route("/")
def homepage():
    """"""
    # 
    
    # 
    
    return render_template("index.html")


from datetime import datetime
from functools import wraps

from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from todo_app import app, login_manager, db
from todo_app.models import User, Task
from todo_app.forms import RegisterUserForm, LoginUserForm, AddTaskForm


@app.context_processor
def inject_now():
    """Injects date."""
    return {"now": datetime.now()}


def users_only(f):
    @wraps
    def func(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(403)
        return f(*args, **kwargs)
    return func

@login_manager.user_loader
def load_user(user_id:int):
    return User.query.get(int(user_id))


@app.route("/", methods=["GET", "POST"])
def homepage():
    """Homepage gives users ability to input tasks into database and displays the tasks."""
    add_task_form = AddTaskForm()

    # Retrieving tasks from db to display in descending order
    tasks = Task.query.order_by(Task.published_date.desc()).all()
    
    incomplete_tasks = Task.query.order_by(Task.published_date.desc()).filter_by(completed=False).all()
    completed_tasks = Task.query.order_by(Task.published_date.desc()).filter_by(completed=True).all()
    
    
    if add_task_form.validate_on_submit():
            
        if not current_user.is_authenticated:
            flash("Sorry...You have to be signed in to do that!")
            return redirect(url_for("user_login"))
        
        new_task = Task(
            author=current_user,
            user_task=add_task_form.user_task.data,
            published_date=datetime.now().strftime("%d/%m/%Y, %I:%M:%S%p %Z")
        )
    
        
        db.session.add(new_task)
        db.session.commit()
        
        return redirect(url_for("homepage"))
    
    return render_template("index.html", 
                           add_task_form=add_task_form,current_user=current_user, all_tasks=tasks, completed_tasks=completed_tasks, incomplete_tasks=incomplete_tasks)


@app.route("/register-user", methods=["GET", "POST"])
def register_user():
    register_form = RegisterUserForm()
    
    if register_form.validate_on_submit():
        hash_and_salted_password = generate_password_hash(
            password=request.form["password"],
            method="pbkdf2:sha256",
            salt_length=8
        )
        
        create_user = User()
        create_user.username = request.form["username"]
        
        # Checkes user table of db for existing user with same username
        existing_user = User.query.filter_by(username=create_user.username).first()
        
        if existing_user:
            flash("That username has been taken already. Please try again.")
            return redirect(url_for("homepage"))
        
        # Creating new user if user has chosen a unique username
        create_user.password = hash_and_salted_password
        
        db.session.add(create_user)
        db.session.commit()
        
        login_user(create_user)
        
        return redirect(url_for("homepage"))
    
    return render_template("reg_login.html", 
                           register_form=register_form, title="Register")


@app.route("/login-user", methods=["GET", "POST"])
def user_login():
    login_form = LoginUserForm()
    
    if login_form.validate_on_submit():
        login_username =  request.form["username"]
        login_password =  request.form["password"]
        
        # Search db for user
        searched_user = User.query.filter_by(username=login_username).first()
        
        if not searched_user:
            flash("That username doesn't exist. Please try again.")
            return redirect(url_for("login_user"))
        elif not check_password_hash(searched_user.password, login_password):
            flash("You entered the wrong password. Please try again.")
            return redirect(url_for("login_user"))
        else:
            # If username & password match existing user, login this user
            login_user(searched_user)
            return redirect(url_for("homepage"))
    
    return render_template("reg_login.html", 
                           login_form=login_form, title="Login", current_user=current_user)


@app.route("/logout")
def logout():
    """"""
    logout_user()
    return redirect(url_for("homepage"))



@app.route("/task-complete/<int:task_id>", methods=["GET", "POST"])
#@login_required
def task_now_complete(task_id: int):
    """Updates 'completed' column to True for a chosen task in db"""
    
    # Redirects to login page if a non-logged in user accesses route
    if not current_user.is_authenticated:
        flash("Sorry... You have to be logged in to do that.")
        return redirect(url_for("user_login"))

    task_to_complete = Task.query.get(task_id)
    task_to_complete.completed = True

    db.session.commit()

    return redirect(url_for("homepage"))



@app.route("/delete-task/<int:task_id>")
def delete_task(task_id: int):
    """"""
    if not current_user.is_authenticated:
        flash("Sorry...You have to be signed in to do that!")
        return redirect(url_for("user_login"))
    
    task_to_delete = Task.query.get(task_id)
    
    db.session.delete(task_to_delete)
    db.session.commit()
    
    return redirect(url_for("homepage"))
    
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField,EmailField, DateField, DateTimeField, SelectField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, URL
from flask_ckeditor import CKEditor


class RegisterUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")
    
    def validate_username(self, username_to_check):
        """
        The provided username is checked in the database to see if 
        it already exists.
        If already used, an error message is given and user will 
        need to submit another username.
        """
        # TODO: Query User table of database to see if entered username already exists in the database
        
        # TODO: If user already exist in the database, raise ValidationError("Error message")
        pass
    
    def validate_email_address(self, email_addr_to_check):
        """
        The provided email address is checked in the database to see 
        if it already exists.
        If already used, an error message is given and user will 
        need to submit another email address or use the existing 
        email address.
        """
        # TODO: Query User table of database to see if entered email address already exists in the database
        
        # TODO: If email address already exists in the database, raise ValidationError("Error message")
        pass
    
    
class LoginUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class AddTaskForm(FlaskForm):
    user_task = StringField("Task", validators=[DataRequired()])
    submit = SubmitField("Add Task")

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Email is required."),  # Error message if the field is empty
        Email(message="Please enter a valid email address.")  # Error message if the format is invalid
    ])
    password = PasswordField('Password', validators=[DataRequired(message="Password is required.")])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username is required."), 
        Length(min=2, max=20, message="Username must be between 2 and 20 characters.")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email is required."), 
        Email(message="Please enter a valid email address.")
    ])
    password = PasswordField('Password', validators=[DataRequired(message="Password is required.")])
    submit = SubmitField('Register')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message="Title is required.")])
    description = TextAreaField('Description')
    submit = SubmitField('Create Task')

class QuickThoughtForm(FlaskForm):
    content = TextAreaField('Quick Thought', validators=[DataRequired(message="Content cannot be empty.")])
    submit = SubmitField('Add Thought')

# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_login import current_user

# Handles user registration with username, email, password, and password confirmation fields. 
# Includes custom validation for username and email uniqueness.
class RegistrationForm(FlaskForm):
    username            = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email               = StringField('Email', validators=[DataRequired(), Email()])
    password            = PasswordField('Password', validators=[DataRequired()])
    confirm_password    = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit              = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

# Handles user login with email, password, and a "Remember Me" option
class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()], render_kw={"class": "form-floating"})
    password = PasswordField(label='Password', validators=[DataRequired()], render_kw={"class": "form-floating"})
    remember    = BooleanField('Remember Me')
    submit      = SubmitField('Login')

# Allows users to update their account details, with custom validation for username and email uniqueness
class UpdateAccountForm(FlaskForm):
    username    = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email       = StringField('Email', validators=[DataRequired(), Email()])
    submit      = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

# Allows users to create and update blog posts with title and content fields
class PostForm(FlaskForm):
    title      = StringField('Title', validators=[DataRequired()])
    content    = TextAreaField('Content', validators=[DataRequired()])
    submit     = SubmitField('Post')

# Allows users to add comments to posts with a content field
class CommentForm(FlaskForm):
    content    = TextAreaField('Comment', validators=[DataRequired()])
    submit     = SubmitField('Comment')

# Allows users to change the password
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Change Password')
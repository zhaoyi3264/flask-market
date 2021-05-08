from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField

class RegisterForm(FlaskForm):
    username = StringField('User Name:')
    email_address = StringField('Email Address:')
    password1 = PasswordField('Password:')
    password2 = PasswordField('Confirm Password:')
    submit = SubmitField('Create Account')
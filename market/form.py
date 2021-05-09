from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from market.model import User

class RegisterForm(FlaskForm):

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('User Name already existed.')
    
    def validate_email_address(self, email_address):
        email = User.query.filter_by(email_address=email_address.data).first()
        if email:
            raise ValidationError('Email Address already existed.')

    username = StringField('User Name:', validators=[DataRequired(), Length(min=2, max=20)])
    email_address = StringField('Email Address:', validators=[DataRequired(), Email()])
    password1 = PasswordField('Password:', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField('Sign In')
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class Loginform(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class Registrationform(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please select different username")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please select different email address")

class Postform(FlaskForm):
    body = StringField('Treść wpisu', validators=[DataRequired()])
    submit = SubmitField('Dodaj post')
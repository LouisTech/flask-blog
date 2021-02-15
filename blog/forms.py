from flask_wtf import FlaskForm
from wtforms.fields.core import StringField
from wtforms import StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError, Regexp
from blog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3, max=15)])
    first_name = StringField('First Name', validators=[
                             DataRequired(), Length(min=1, max=49)])
    last_name = StringField('Last Name', validators=[
                            DataRequired(), Length(min=1, max=49)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Regexp(
        '^.{6,8}$', message='Your password should be between 6 and 8 characters long')])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('Username taken.')


    def validate_email(self, email):
        db_email = User.query.filter_by(email=email.data).first()

        if db_email:
            raise ValidationError('You already have an account. Please Login.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    #Need to add validation here
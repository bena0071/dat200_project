from flask.app import Flask
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from flask_recaptcha.recaptcha3 import Recaptcha3Field


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    recaptcha = Recaptcha3Field(action="Login", execute_on_load=True)
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(
        min=12, max=128, message="Password must have at least 12 characters.")])
    password2 = PasswordField('Repeat Password', validators=[
                              DataRequired(), EqualTo('password')])
    recaptcha = Recaptcha3Field(action="Register", execute_on_load=True)
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Invalid username!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Invalid email address!')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Invalid username!')


class PostForm(FlaskForm):
    post = TextAreaField('Post something!', validators=[
                         DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Post')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    comment = TextAreaField('Write a comment', validators=[
                            DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Comment')

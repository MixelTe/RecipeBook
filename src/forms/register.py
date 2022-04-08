from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, IntegerField, ValidationError
from wtforms.validators import DataRequired
from data import db_session
from data.users import User


def passwordCheck(form, field):
    if field.data != form.password.data:
        raise ValidationError('Passwords do not match')


def userExistCheck(form, field):
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.email == field.data).first():
        raise ValidationError('User with this login already exists')


class RegisterForm(FlaskForm):
    email = EmailField('Login / email', validators=[DataRequired(), userExistCheck])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired(), passwordCheck])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


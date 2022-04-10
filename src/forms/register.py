from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, ValidationError
from wtforms.validators import DataRequired
from data import db_session
from data.users import User


def passwordCheck(form, field):
    if field.data != form.password.data:
        raise ValidationError('Пароли не совпадают')


def userExistCheck(form, field):
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.email == field.data).first():
        raise ValidationError('Пользователь с таким email уже существует')


class RegisterForm(FlaskForm):
    name = StringField('Как к вам обращаться?', validators=[DataRequired("Необходимо заполнить")])
    email = EmailField('Ваш email', validators=[DataRequired("Необходимо заполнить"), userExistCheck])
    password = PasswordField('Пароль', validators=[DataRequired("Необходимо заполнить")])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired("Необходимо заполнить"), passwordCheck])
    submit = SubmitField('Зарегестрироваться')


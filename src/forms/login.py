from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField
import wtforms
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = wtforms.EmailField('Email', validators=[DataRequired("Необходимо заполнить")])
    password = PasswordField('Пароль', validators=[DataRequired("Необходимо заполнить")])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

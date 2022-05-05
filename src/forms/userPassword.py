from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired


def passwordCheck(form, field):
    if field.data != form.password_new.data:
        raise ValidationError('Пароли не совпадают')


def checkPassword(form, field):
    if (not current_user.check_password(field.data)):
        raise ValidationError('Неверный пароль')


class UserPasswordForm(FlaskForm):
    password_old = PasswordField('Текущий пароль', validators=[DataRequired("Необходимо заполнить"), checkPassword])
    password_new = PasswordField('Новый пароль', validators=[DataRequired("Необходимо заполнить")])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired("Необходимо заполнить"), passwordCheck])
    submit = SubmitField('Сохранить')

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


def getName():
    return current_user.name


class UserNameForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired("Необходимо заполнить")], default=getName)
    submit = SubmitField('Сохранить')

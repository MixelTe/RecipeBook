from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, ValidationError, SelectField, SelectMultipleField, EmailField
from wtforms.validators import DataRequired
from data import db_session
from data.users import User


def userExistCheck(form, field: IntegerField):
    db_sess = db_session.create_session()
    if not db_sess.query(User).get(field.data):
        raise ValidationError('User with this id does not exists')


class DepartmentForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    chief = SelectField("Сhief", coerce=int, validators=[DataRequired(), userExistCheck])
    members = SelectMultipleField("Members", coerce=int)
    email = EmailField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def init(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        choices = [(user.id, f"{user.name} {user.surname}") for user in users]
        self.chief.choices = choices
        self.members.choices = choices
        return self

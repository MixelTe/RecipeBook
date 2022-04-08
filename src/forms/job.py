from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, IntegerField, DateField, ValidationError, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, NumberRange, Optional
from data import db_session
from data.users import User


def userExistCheck(form, field: IntegerField):
    db_sess = db_session.create_session()
    if not db_sess.query(User).get(field.data):
        raise ValidationError('User with this id does not exists')


def collaboratorsExistCheck(form, field: StringField):
    collaborators = field.data.split(",")
    db_sess = db_session.create_session()
    for collaborator in collaborators:
        if not db_sess.query(User).get(collaborator):
            raise ValidationError(f'User with id "{collaborator}" does not exists')


class JobForm(FlaskForm):
    job = StringField("Job Title", validators=[DataRequired()])
    team_leader = SelectField("Team Leader", coerce=int, validators=[DataRequired(), userExistCheck])
    # team_leader = IntegerField("Team Leader Id", validators=[DataRequired(), NumberRange(min=0), userExistCheck])
    work_size = IntegerField("Work Size", validators=[DataRequired(), NumberRange(min=0)])
    collaborators = SelectMultipleField("Collaborators", coerce=int)
    # collaborators = StringField("Collaborator IDs (comma-separated)", validators=[Optional(), collaboratorsExistCheck])
    start_date = DateField("Start Date", default=datetime.now, validators=[DataRequired()])
    end_date = DateField("End Date", validators=[Optional()])
    is_finished = BooleanField("Is Job finished?")
    submit = SubmitField("Submit")

    def init(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        choices = [(user.id, f"{user.name} {user.surname}") for user in users]
        self.team_leader.choices = choices
        self.collaborators.choices = choices
        return self

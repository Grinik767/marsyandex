from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class AddingJob(FlaskForm):
    title = StringField('Job title', validators=[DataRequired()])
    tl_id = IntegerField('Team Leader id', validators=[DataRequired()])
    work_size = IntegerField('Work size', validators=[DataRequired()])
    collabs = StringField('Collaborators', validators=[DataRequired()])
    is_fin = BooleanField('Is job finished?')
    submit = SubmitField('Submit')
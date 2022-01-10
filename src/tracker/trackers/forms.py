from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Regexp


class NewTracker(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Regexp(r"^[\w ]+$")])
    desc = StringField("Description", validators=[DataRequired()])

    submit = SubmitField("Add Tracker")


class EditTracker(FlaskForm):
    name = StringField("Pretty Name", validators=[DataRequired(), Regexp(r"^[\w ]+$")])
    desc = StringField("Description", validators=[DataRequired()])

    submit = SubmitField("Apply Changes")

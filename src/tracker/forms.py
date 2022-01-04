from flask_wtf import FlaskForm
from wtforms import StringField

from wtforms.fields.simple import BooleanField, SubmitField
from wtforms.validators import DataRequired, Regexp
from wtforms.fields import DateTimeLocalField
from datetime import datetime


class NewTracker(FlaskForm):
    name_id = StringField("Name ID", validators=[DataRequired(), Regexp(r"^[\w_-]+$")])
    name = StringField("Pretty Name", validators=[DataRequired(), Regexp(r"^[\w ]+$")])
    desc = StringField(
        "Description", validators=[DataRequired(), Regexp(r"^[\w _\-!.,]+$")]
    )

    submit = SubmitField("Add Tracker")


class NewApplication(FlaskForm):
    company_name = StringField(
        "Company Name", validators=[DataRequired(), Regexp(r"^[\w ]+$")]
    )
    position_name = StringField(
        "Position Name", validators=[DataRequired(), Regexp(r"^[\w ]+$")]
    )
    # source =
    # link = StringField("Link")
    # status = StringField("Status")

    submit = SubmitField("Add Application")


class NewEvent(FlaskForm):
    desc = StringField("Description", validators=[DataRequired(), Regexp(r"^[\w ]+$")])
    from_me = BooleanField("From me?")
    date = DateTimeLocalField(
        "Date",
        default=datetime.now,
        validators=[DataRequired()],
    )

    submit = SubmitField("Add Event")

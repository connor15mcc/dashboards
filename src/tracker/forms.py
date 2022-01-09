from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.choices import RadioField, SelectField
from wtforms.fields.simple import SubmitField, URLField
from wtforms.validators import DataRequired, Regexp, AnyOf
from wtforms.fields import DateTimeLocalField
from datetime import datetime


class NewTracker(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Regexp(r"^[\w ]+$")])
    desc = StringField("Description", validators=[DataRequired()])

    submit = SubmitField("Add Tracker")


class NewApplication(FlaskForm):
    company_name = StringField("Company Name", validators=[DataRequired()])
    position_name = StringField("Position Name", validators=[DataRequired()])
    source = SelectField(
        "Source",
        choices=[
            ("LinkedIn", "LinkedIn"),
            ("Handshake", "Handshake"),
            ("Indeed", "Indeed"),
            ("Other", "Other"),
        ],
    )
    link = URLField("URL", validators=[])

    submit = SubmitField("Add Application")


class NewEvent(FlaskForm):
    desc = StringField("Description", validators=[DataRequired()])
    from_me = RadioField(
        "From:",
        choices=[
            ("true", "Me"),
            ("false", "The Company"),
        ],
        coerce=lambda x: True if x == "true" else False,
        validators=[AnyOf([True, False])],
    )
    action_necessary = RadioField(
        "Action Necessary:",
        choices=[
            ("true", "Yes"),
            ("false", "No"),
        ],
        coerce=lambda x: True if x == "true" else False,
        validators=[AnyOf([True, False])],
    )
    date = DateTimeLocalField(
        "Date",
        default=datetime.now,
        validators=[DataRequired()],
    )

    submit = SubmitField("Add Event")


class EditTracker(FlaskForm):
    name = StringField("Pretty Name", validators=[DataRequired(), Regexp(r"^[\w ]+$")])
    desc = StringField("Description", validators=[DataRequired()])

    submit = SubmitField("Apply Changes")


class EditApplication(FlaskForm):
    company_name = StringField("Company Name", validators=[DataRequired()])
    position_name = StringField("Position Name", validators=[DataRequired()])
    source = SelectField(
        "Source",
        choices=[
            ("LinkedIn", "LinkedIn"),
            ("Handshake", "Handshake"),
            ("Indeed", "Indeed"),
            ("Other", "Other"),
        ],
    )
    link = URLField("URL", validators=[])
    status = SelectField(
        "Status",
        choices=[
            ("Found", "Found"),
            ("Applied", "Applied"),
            ("Accepted", "Accepted"),
            ("Rejected", "Rejected"),
        ],
    )

    submit = SubmitField("Apply Changes")


class EditEvent(FlaskForm):
    desc = StringField("Description", validators=[DataRequired()])
    from_me = RadioField(
        "From:",
        choices=[
            ("true", "Me"),
            ("false", "The Company"),
        ],
        coerce=lambda x: True if x == "true" else False,
        validators=[AnyOf([True, False])],
    )
    action_necessary = RadioField(
        "Action Necessary:",
        choices=[
            ("true", "Yes"),
            ("false", "No"),
        ],
        coerce=lambda x: True if x == "true" else False,
        validators=[AnyOf([True, False])],
    )
    date = DateTimeLocalField(
        "Date",
        default=datetime.now,
        validators=[DataRequired()],
    )

    submit = SubmitField("Apply Changes")

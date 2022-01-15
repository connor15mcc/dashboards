from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.choices import RadioField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, AnyOf
from wtforms.fields import DateTimeLocalField
from datetime import datetime


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

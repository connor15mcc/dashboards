from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import SubmitField, URLField
from wtforms.validators import DataRequired


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
    addr1 = StringField("Street Address", validators=[])
    addr2 = StringField("City Address", validators=[])

    submit = SubmitField("Add Application")


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
    addr1 = StringField("Street Address", validators=[])
    addr2 = StringField("City Address", validators=[])
    status = SelectField(
        "Status",
        choices=[
            ("Initialized", "Initialized"),
            ("Applied", "Applied"),
            ("Accepted", "Accepted"),
            ("Rejected", "Rejected"),
        ],
    )

    submit = SubmitField("Apply Changes")

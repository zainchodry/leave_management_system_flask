from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    TextAreaField,
    IntegerField,
    SubmitField
)

from wtforms.validators import (
    DataRequired
)

class DepartmentForm(
    FlaskForm
):

    name = StringField(
        "Department Name",
        validators=[
            DataRequired()
        ]
    )

    description = TextAreaField(
        "Description"
    )

    head_id = IntegerField(
        "Department Head ID"
    )

    submit = SubmitField(
        "Save Department"
    )

class UpdateDepartmentForm(
    FlaskForm
):

    name = StringField(
        "Department Name",
        validators=[
            DataRequired()
        ]
    )

    description = TextAreaField(
        "Description"
    )

    head_id = IntegerField(
        "Department Head ID"
    )

    submit = SubmitField(
        "Update Department"
    )


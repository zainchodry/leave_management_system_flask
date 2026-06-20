from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    TextAreaField,
    FileField,
    SubmitField
)

from wtforms.validators import (
    Optional
)

class ProfileForm(
    FlaskForm
):

    profile_picture = FileField(
        "Profile Picture"
    )

    phone_number = StringField(
        "Phone Number"
    )

    address = TextAreaField(
        "Address"
    )

    department = StringField(
        "Department"
    )

    submit = SubmitField(
        "Update Profile"
    )


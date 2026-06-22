from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class UpdateUserRoleForm(FlaskForm):
    role = SelectField(
        "Role",
        choices=[
            ("STUDENT",  "Student"),
            ("TEACHER",  "Teacher"),
            ("ADMIN",    "Admin"),
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField("Update Role")

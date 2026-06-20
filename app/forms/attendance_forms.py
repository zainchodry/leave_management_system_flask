from flask_wtf import FlaskForm

from wtforms import (
    SelectField,
    DateField,
    IntegerField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import (
    DataRequired
)

class AttendanceForm(
    FlaskForm
):

    student_id = IntegerField(
        "Student ID",
        validators=[
            DataRequired()
        ]
    )

    date = DateField(
        "Date",
        validators=[
            DataRequired()
        ]
    )

    status = SelectField(
        "Status",
        choices=[
            ("PRESENT", "Present"),
            ("ABSENT", "Absent"),
            ("LEAVE", "Leave")
        ]
    )

    remarks = TextAreaField(
        "Remarks"
    )

    submit = SubmitField(
        "Mark Attendance"
    )

class UpdateAttendanceForm(
    FlaskForm
):

    status = SelectField(
        "Status",
        choices=[
            ("PRESENT", "Present"),
            ("ABSENT", "Absent"),
            ("LEAVE", "Leave")
        ]
    )

    remarks = TextAreaField(
        "Remarks"
    )

    submit = SubmitField(
        "Update Attendance"
    )


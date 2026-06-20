from flask_wtf import FlaskForm

from wtforms import (
    SelectField,
    DateField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import (
    DataRequired
)

class LeaveForm(
    FlaskForm
):

    leave_type = SelectField(
        "Leave Type",
        choices=[
            ("SICK", "Sick"),
            ("CASUAL", "Casual"),
            ("EMERGENCY", "Emergency")
        ]
    )

    start_date = DateField(
        "Start Date",
        validators=[
            DataRequired()
        ]
    )

    end_date = DateField(
        "End Date",
        validators=[
            DataRequired()
        ]
    )

    reason = TextAreaField(
        "Reason",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField(
        "Apply Leave"
    )

class LeaveReviewForm(
    FlaskForm
):

    status = SelectField(
        "Status",
        choices=[
            ("APPROVED", "Approve"),
            ("REJECTED", "Reject")
        ]
    )

    teacher_remark = TextAreaField(
        "Remark"
    )

    submit = SubmitField(
        "Submit"
    )


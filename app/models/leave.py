from datetime import datetime

from app.extensions import db


class LeaveRequest(
    db.Model
):

    __tablename__ = "leave_requests"

    LEAVE_TYPES = (
        "SICK",
        "CASUAL",
        "EMERGENCY"
    )

    STATUS_CHOICES = (
        "PENDING",
        "APPROVED",
        "REJECTED",
        "CANCELLED"
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    leave_type = db.Column(
        db.Enum(*LEAVE_TYPES, name="leave_types"),default="CASUAL",
        nullable=False
    )

    start_date = db.Column(
        db.Date,
        nullable=False
    )

    end_date = db.Column(
        db.Date,
        nullable=False
    )

    reason = db.Column(
        db.Text,
        nullable=False
    )

    teacher_remark = db.Column(
        db.Text
    )

    status = db.Column(
        db.Enum(*STATUS_CHOICES, name="leave_statuses"),
        default="PENDING"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    student = db.relationship(
        "User",
        backref="leave_requests"
    )

    def __repr__(self):

        return (
            f"{self.student.email}"
            f" - {self.status}"
        )

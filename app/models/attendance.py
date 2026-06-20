from datetime import datetime

from app.extensions import db


class Attendance(
    db.Model
):

    __tablename__ = "attendance"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    marked_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    date = db.Column(
        db.Date,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False
    )

    remarks = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    student = db.relationship(
        "User",
        foreign_keys=[student_id]
    )

    teacher = db.relationship(
        "User",
        foreign_keys=[marked_by]
    )

    __table_args__ = (

        db.UniqueConstraint(
            "student_id",
            "date",
            name="unique_student_attendance"
        ),
    )

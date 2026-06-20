from datetime import datetime

from app.extensions import db


class Department(
    db.Model
):

    __tablename__ = "departments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    head_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    department_head = db.relationship(
        "User",
        foreign_keys=[head_id]
    )

    def __repr__(self):

        return self.name

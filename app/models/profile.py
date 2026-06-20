from datetime import datetime

from app.extensions import db


class Profile(
    db.Model
):

    __tablename__ = "profiles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    profile_picture = db.Column(
        db.String(500)
    )

    phone_number = db.Column(
        db.String(20)
    )

    address = db.Column(
        db.Text
    )

    department = db.Column(
        db.String(255)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):

        return f"{self.user.email}"

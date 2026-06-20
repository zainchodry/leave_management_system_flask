from datetime import datetime

from app.extensions import db


class PasswordResetOTP(
    db.Model
):

    __tablename__ = "password_reset_otps"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    otp = db.Column(
        db.String(6),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref="reset_otps"
    )

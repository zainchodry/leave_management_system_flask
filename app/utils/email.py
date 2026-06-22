"""
Email utility helpers.

For real email delivery, set MAIL_USERNAME and MAIL_PASSWORD in your .env file.
In development (no credentials set), emails are printed to the console instead.
"""
from flask import current_app, render_template
from flask_mail import Message
from app.extensions import mail


def _send(subject: str, recipient: str, html_body: str) -> None:
    """Internal: send an email or fall back to console output."""
    username = current_app.config.get("MAIL_USERNAME", "")

    if not username:
        # Dev mode — print to console
        print("=" * 60)
        print(f"[EMAIL - DEV MODE]  To: {recipient}")
        print(f"Subject: {subject}")
        print(html_body)
        print("=" * 60)
        return

    msg = Message(
        subject=subject,
        recipients=[recipient],
        html=html_body,
    )
    mail.send(msg)


def send_otp_email(user, otp: str) -> None:
    """Send a password-reset OTP to the user."""
    html = render_template(
        "email/otp_email.html",
        user=user,
        otp=otp,
        expiry_minutes=current_app.config.get("OTP_EXPIRY_MINUTES", 10),
    )
    _send(
        subject="Your Password Reset OTP — EduLeave",
        recipient=user.email,
        html_body=html,
    )


def send_leave_status_email(leave) -> None:
    """Notify a student that their leave status has been updated."""
    html = render_template(
        "email/leave_status_email.html",
        leave=leave,
        student=leave.student,
    )
    status_label = leave.status.capitalize()
    _send(
        subject=f"Leave Request {status_label} — EduLeave",
        recipient=leave.student.email,
        html_body=html,
    )


def send_leave_applied_email(leave, teachers) -> None:
    """Notify all teachers that a new leave request was submitted."""
    html = render_template(
        "email/leave_applied_email.html",
        leave=leave,
        student=leave.student,
    )
    for teacher in teachers:
        _send(
            subject=f"New Leave Request from {leave.student.username} — EduLeave",
            recipient=teacher.email,
            html_body=html,
        )

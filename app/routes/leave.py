from flask import (
    Blueprint, render_template, redirect, url_for, flash
)
from flask_login import login_required, current_user

from app.models import LeaveRequest, Notification, User
from app.forms import LeaveForm, LeaveReviewForm
from app.utils.decorators import student_required, teacher_required
from app.utils.email import send_leave_status_email, send_leave_applied_email
from app.extensions import db

leave_bp = Blueprint("leave", __name__)


@leave_bp.route("/leave/apply", methods=["GET", "POST"])
@login_required
@student_required
def apply_leave():
    form = LeaveForm()

    if form.validate_on_submit():
        if form.start_date.data > form.end_date.data:
            flash("Start date cannot be after end date.", "danger")
            return redirect(url_for("leave.apply_leave"))

        leave = LeaveRequest(
            student_id=current_user.id,
            leave_type=form.leave_type.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            reason=form.reason.data,
        )
        db.session.add(leave)
        db.session.commit()

        # Notify all teachers in DB + send email
        teachers = User.query.filter_by(role="TEACHER").all()
        for teacher in teachers:
            notification = Notification(
                receiver_id=teacher.id,
                title="New Leave Request",
                message=f"{current_user.username} applied for {leave.leave_type} leave.",
                notification_type="LEAVE_APPLIED",
            )
            db.session.add(notification)
        db.session.commit()

        # Send email notifications to all teachers
        try:
            send_leave_applied_email(leave, teachers)
        except Exception as e:
            pass  # Don't fail the request if email fails

        flash("Leave application submitted successfully!", "success")
        return redirect(url_for("leave.my_leaves"))

    return render_template("leave/apply_leave.html", form=form)


@leave_bp.route("/leave/my-leaves")
@login_required
@student_required
def my_leaves():
    leaves = LeaveRequest.query.filter_by(
        student_id=current_user.id
    ).order_by(LeaveRequest.created_at.desc()).all()
    return render_template("leave/my_leaves.html", leaves=leaves)


@leave_bp.route("/leave/cancel/<int:id>")
@login_required
@student_required
def cancel_leave(id):
    leave = LeaveRequest.query.get_or_404(id)

    if leave.student_id != current_user.id:
        flash("You are not authorised to cancel this request.", "danger")
        return redirect(url_for("leave.my_leaves"))

    if leave.status != "PENDING":
        flash("Only pending leaves can be cancelled.", "warning")
        return redirect(url_for("leave.my_leaves"))

    leave.status = "CANCELLED"
    db.session.commit()

    flash("Leave request cancelled.", "success")
    return redirect(url_for("leave.my_leaves"))


@leave_bp.route("/leave/pending")
@login_required
@teacher_required
def pending_leaves():
    leaves = LeaveRequest.query.filter_by(
        status="PENDING"
    ).order_by(LeaveRequest.created_at.desc()).all()
    return render_template("leave/pending_leaves.html", leaves=leaves)


@leave_bp.route("/leave/all")
@login_required
@teacher_required
def all_leaves():
    leaves = LeaveRequest.query.order_by(LeaveRequest.created_at.desc()).all()
    return render_template("leave/all_leaves.html", leaves=leaves)


@leave_bp.route("/leave/review/<int:id>", methods=["GET", "POST"])
@login_required
@teacher_required
def review_leave(id):
    leave = LeaveRequest.query.get_or_404(id)
    form  = LeaveReviewForm(obj=leave)

    if form.validate_on_submit():
        leave.status         = form.status.data
        leave.teacher_remark = form.teacher_remark.data
        db.session.commit()

        # In-app notification for student
        notification = Notification(
            receiver_id=leave.student_id,
            title="Leave Status Updated",
            message=(
                f"Your {leave.leave_type} leave request has been "
                f"{leave.status.lower()}."
            ),
            notification_type=(
                "LEAVE_APPROVED" if leave.status == "APPROVED" else "LEAVE_REJECTED"
            ),
        )
        db.session.add(notification)
        db.session.commit()

        # Email notification
        try:
            send_leave_status_email(leave)
        except Exception:
            pass

        flash("Leave review submitted successfully.", "success")
        return redirect(url_for("leave.pending_leaves"))

    return render_template("leave/review_leave.html", form=form, leave=leave)

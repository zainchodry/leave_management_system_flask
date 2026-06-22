from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import LeaveRequest, Attendance, User, Notification
from app.extensions import db

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def home():
    if current_user.role == "ADMIN":
        total_users       = User.query.count()
        total_students    = User.query.filter_by(role="STUDENT").count()
        total_teachers    = User.query.filter_by(role="TEACHER").count()
        pending_leaves    = LeaveRequest.query.filter_by(status="PENDING").count()
        approved_leaves   = LeaveRequest.query.filter_by(status="APPROVED").count()
        rejected_leaves   = LeaveRequest.query.filter_by(status="REJECTED").count()
        total_attendance  = Attendance.query.count()
        present_count     = Attendance.query.filter_by(status="PRESENT").count()
        absent_count      = Attendance.query.filter_by(status="ABSENT").count()
        recent_leaves     = (
            LeaveRequest.query
            .order_by(LeaveRequest.created_at.desc())
            .limit(5).all()
        )
        return render_template(
            "dashboard/admin_dashboard.html",
            total_users=total_users,
            total_students=total_students,
            total_teachers=total_teachers,
            pending_leaves=pending_leaves,
            approved_leaves=approved_leaves,
            rejected_leaves=rejected_leaves,
            total_attendance=total_attendance,
            present_count=present_count,
            absent_count=absent_count,
            recent_leaves=recent_leaves,
        )

    if current_user.role == "TEACHER":
        pending_leaves   = LeaveRequest.query.filter_by(status="PENDING").count()
        approved_today   = LeaveRequest.query.filter_by(status="APPROVED").count()
        total_students   = User.query.filter_by(role="STUDENT").count()
        recent_leaves    = (
            LeaveRequest.query
            .filter_by(status="PENDING")
            .order_by(LeaveRequest.created_at.desc())
            .limit(5).all()
        )
        return render_template(
            "dashboard/teacher_dashboard.html",
            pending_leaves=pending_leaves,
            approved_today=approved_today,
            total_students=total_students,
            recent_leaves=recent_leaves,
        )

    # Student dashboard
    my_leaves        = LeaveRequest.query.filter_by(student_id=current_user.id)
    total_applied    = my_leaves.count()
    pending_count    = my_leaves.filter_by(status="PENDING").count()
    approved_count   = LeaveRequest.query.filter_by(
        student_id=current_user.id, status="APPROVED"
    ).count()
    rejected_count   = LeaveRequest.query.filter_by(
        student_id=current_user.id, status="REJECTED"
    ).count()
    attendance_days  = Attendance.query.filter_by(
        student_id=current_user.id, status="PRESENT"
    ).count()
    recent_leaves    = (
        LeaveRequest.query
        .filter_by(student_id=current_user.id)
        .order_by(LeaveRequest.created_at.desc())
        .limit(5).all()
    )
    recent_notifications = (
        Notification.query
        .filter_by(receiver_id=current_user.id)
        .order_by(Notification.created_at.desc())
        .limit(5).all()
    )
    return render_template(
        "dashboard/student_dashboard.html",
        total_applied=total_applied,
        pending_count=pending_count,
        approved_count=approved_count,
        rejected_count=rejected_count,
        attendance_days=attendance_days,
        recent_leaves=recent_leaves,
        recent_notifications=recent_notifications,
    )
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from app.models import (
    Attendance,
    Notification
)

from app.forms import (
    AttendanceForm,
    UpdateAttendanceForm
)

from app.utils.decorators import (
    teacher_required,
    student_required,
    admin_required
)

attendance_bp = Blueprint(
    "attendance",
    __name__
)

from app.extensions import db

@attendance_bp.route(
    "/attendance/mark",
    methods=["GET", "POST"]
)
@login_required
@teacher_required
def mark_attendance():

    form = AttendanceForm()

    if form.validate_on_submit():

        attendance = Attendance(

            student_id=form.student_id.data,

            marked_by=current_user.id,

            date=form.date.data,

            status=form.status.data,

            remarks=form.remarks.data
        )

        db.session.add(
            attendance
        )

        notification = Notification(

            receiver_id=form.student_id.data,

            title="Attendance Marked",

            message="Your attendance has been marked.",

            notification_type="ATTENDANCE_MARKED"
        )

        db.session.add(
            notification
        )

        db.session.commit()

        flash(
            "Attendance Marked",
            "success"
        )

        return redirect(
            url_for(
                "attendance.mark_attendance"
            )
        )

    return render_template(
        "attendance/mark_attendance.html",
        form=form
    )

@attendance_bp.route(
    "/attendance/my"
)
@login_required
@student_required
def my_attendance():

    attendance = Attendance.query.filter_by(
        student_id=current_user.id
    ).all()

    return render_template(
        "attendance/my_attendance.html",
        attendance=attendance
    )

@attendance_bp.route(
    "/attendance/statistics"
)
@login_required
@admin_required
def attendance_statistics():

    total = Attendance.query.count()

    present = Attendance.query.filter_by(
        status="PRESENT"
    ).count()

    absent = Attendance.query.filter_by(
        status="ABSENT"
    ).count()

    leave = Attendance.query.filter_by(
        status="LEAVE"
    ).count()

    return render_template(

        "attendance/statistics.html",

        total=total,

        present=present,

        absent=absent,

        leave=leave
    )

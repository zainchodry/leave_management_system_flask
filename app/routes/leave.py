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
    LeaveRequest,
    Notification,
    User
)

from app.forms import (
    LeaveForm,
    LeaveReviewForm
)

from app.utils.decorators import (
    student_required,
    teacher_required,
    admin_required
)

from app.extensions import db

leave_bp = Blueprint(
    "leave",
    __name__
)

@leave_bp.route(
    "/leave/apply",
    methods=["GET", "POST"]
)
@login_required
@student_required
def apply_leave():

    form = LeaveForm()

    if form.validate_on_submit():

        leave = LeaveRequest(

            student_id=current_user.id,

            leave_type=form.leave_type.data,

            start_date=form.start_date.data,

            end_date=form.end_date.data,

            reason=form.reason.data
        )

        db.session.add(leave)
        db.session.commit()

        teachers = User.query.filter_by(
            role="TEACHER"
        ).all()

        for teacher in teachers:

            notification = Notification(

                receiver_id=teacher.id,

                title="New Leave Request",

                message=f"{current_user.username} applied for leave",

                notification_type="LEAVE_APPLIED"
            )

            db.session.add(
                notification
            )

        db.session.commit()

        flash(
            "Leave Applied Successfully",
            "success"
        )

        return redirect(
            url_for(
                "leave.my_leaves"
            )
        )

    return render_template(
        "leave/apply_leave.html",
        form=form
    )

@leave_bp.route(
    "/leave/my-leaves"
)
@login_required
@student_required
def my_leaves():

    leaves = LeaveRequest.query.filter_by(
        student_id=current_user.id
    ).all()

    return render_template(
        "leave/my_leaves.html",
        leaves=leaves
    )

@leave_bp.route(
    "/leave/cancel/<int:id>"
)
@login_required
@student_required
def cancel_leave(id):

    leave = LeaveRequest.query.get_or_404(
        id
    )

    if leave.student_id != current_user.id:

        flash(
            "Unauthorized",
            "danger"
        )

        return redirect(
            url_for(
                "leave.my_leaves"
            )
        )

    leave.status = "CANCELLED"

    db.session.commit()

    flash(
        "Leave Cancelled",
        "success"
    )

    return redirect(
        url_for(
            "leave.my_leaves"
        )
    )

@leave_bp.route(
    "/leave/pending"
)
@login_required
@teacher_required
def pending_leaves():

    leaves = LeaveRequest.query.filter_by(
        status="PENDING"
    ).all()

    return render_template(
        "leave/pending_leaves.html",
        leaves=leaves
    )

@leave_bp.route(
    "/leave/review/<int:id>",
    methods=["GET", "POST"]
)
@login_required
@teacher_required
def review_leave(id):

    leave = LeaveRequest.query.get_or_404(
        id
    )

    form = LeaveReviewForm(
        obj=leave
    )

    if form.validate_on_submit():

        leave.status = form.status.data

        leave.teacher_remark = (
            form.teacher_remark.data
        )

        db.session.commit()

        notification = Notification(

            receiver_id=leave.student_id,

            title="Leave Status Updated",

            message=f"Your leave was {leave.status}",

            notification_type=(
                "LEAVE_APPROVED"
                if leave.status == "APPROVED"
                else "LEAVE_REJECTED"
            )
        )

        db.session.add(
            notification
        )

        db.session.commit()

        flash(
            "Leave Reviewed",
            "success"
        )

        return redirect(
            url_for(
                "leave.pending_leaves"
            )
        )

    return render_template(
        "leave/review_leave.html",
        form=form,
        leave=leave
    )


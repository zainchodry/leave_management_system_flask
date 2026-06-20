from flask import (
    Blueprint,
    render_template
)

from flask_login import (
    login_required,
    current_user
)

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)

@dashboard_bp.route("/")
@login_required
def home():

    if current_user.role == "ADMIN":

        return render_template(
            "dashboard/admin_dashboard.html"
        )

    if current_user.role == "TEACHER":

        return render_template(
            "dashboard/teacher_dashboard.html"
        )

    return render_template(
        "dashboard/student_dashboard.html"
    )
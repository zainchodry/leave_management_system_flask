from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for
)

from flask_login import (
    login_required,
    current_user
)

from app.models import (
    Notification
)

from app.extensions import db

notification_bp = Blueprint(
    "notification",
    __name__
)

@notification_bp.route(
    "/notifications"
)
@login_required
def notifications():

    notifications = Notification.query.filter_by(
        receiver_id=current_user.id
    ).all()

    return render_template(
        "notifications/list.html",
        notifications=notifications
    )

@notification_bp.route(
    "/notification/read/<int:id>"
)
@login_required
def mark_read(id):

    notification = Notification.query.get_or_404(
        id
    )

    notification.is_read = True

    db.session.commit()

    return redirect(
        url_for(
            "notification.notifications"
        )
    )


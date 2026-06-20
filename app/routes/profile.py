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
    Profile
)

from app.forms import (
    ProfileForm
)

from app.extensions import db

profile_bp = Blueprint(
    "profile",
    __name__
)

@profile_bp.route("/profile")
@login_required
def profile():

    profile = Profile.query.filter_by(
        user_id=current_user.id
    ).first()

    return render_template(
        "profile/profile.html",
        profile=profile
    )

@profile_bp.route(
    "/profile/update",
    methods=["GET", "POST"]
)
@login_required
def update_profile():

    profile = Profile.query.filter_by(
        user_id=current_user.id
    ).first()

    form = ProfileForm(
        obj=profile
    )

    if form.validate_on_submit():

        profile.phone_number = (
            form.phone_number.data
        )

        profile.address = (
            form.address.data
        )

        profile.department = (
            form.department.data
        )

        db.session.commit()

        flash(
            "Profile Updated",
            "success"
        )

        return redirect(
            url_for(
                "profile.profile"
            )
        )

    return render_template(
        "profile/update_profile.html",
        form=form
    )


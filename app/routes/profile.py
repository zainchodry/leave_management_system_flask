import os
from flask import (
    Blueprint, render_template, redirect, url_for, flash, current_app, request
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models import Profile
from app.forms import ProfileForm
from app.extensions import db

profile_bp = Blueprint("profile", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@profile_bp.route("/profile")
@login_required
def profile():
    prof = Profile.query.filter_by(user_id=current_user.id).first()
    return render_template("profile/profile.html", profile=prof)


@profile_bp.route("/profile/update", methods=["GET", "POST"])
@login_required
def update_profile():
    prof = Profile.query.filter_by(user_id=current_user.id).first()
    form = ProfileForm(obj=prof)

    if form.validate_on_submit():
        prof.phone_number = form.phone_number.data
        prof.address      = form.address.data
        prof.department   = form.department.data

        file = request.files.get("profile_picture")
        if file and file.filename and _allowed_file(file.filename):
            filename = secure_filename(f"user_{current_user.id}_{file.filename}")
            upload_path = current_app.config["UPLOAD_FOLDER"]
            file.save(os.path.join(upload_path, filename))
            prof.profile_picture = f"uploads/profiles/{filename}"

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile.profile"))

    return render_template("profile/update_profile.html", form=form, profile=prof)

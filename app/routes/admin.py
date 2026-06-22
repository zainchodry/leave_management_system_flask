from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User
from app.forms import UpdateUserRoleForm
from app.extensions import db
from app.utils.decorators import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/users")
@login_required
@admin_required
def users():
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=all_users)


@admin_bp.route("/users/<int:id>/role", methods=["GET", "POST"])
@login_required
@admin_required
def update_user_role(id):
    user = User.query.get_or_404(id)

    if user.id == current_user.id:
        flash("You cannot change your own role.", "warning")
        return redirect(url_for("admin.users"))

    form = UpdateUserRoleForm(obj=user)

    if form.validate_on_submit():
        user.role = form.role.data
        db.session.commit()
        flash(f"Role updated for {user.username}.", "success")
        return redirect(url_for("admin.users"))

    return render_template("admin/update_user.html", form=form, user=user)


@admin_bp.route("/users/<int:id>/toggle-active")
@login_required
@admin_required
def toggle_user_active(id):
    user = User.query.get_or_404(id)

    if user.id == current_user.id:
        flash("You cannot deactivate your own account.", "warning")
        return redirect(url_for("admin.users"))

    user.is_active = not user.is_active
    db.session.commit()
    status = "activated" if user.is_active else "deactivated"
    flash(f"User {user.username} has been {status}.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/users/<int:id>/delete")
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)

    if user.id == current_user.id:
        flash("You cannot delete your own account.", "warning")
        return redirect(url_for("admin.users"))

    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.username} has been deleted.", "success")
    return redirect(url_for("admin.users"))

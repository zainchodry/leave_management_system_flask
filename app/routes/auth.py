from datetime import datetime, timedelta

from flask import (
    Blueprint, render_template, redirect, url_for, flash, current_app
)
from flask_login import (
    login_user, logout_user, login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import User, Profile, PasswordResetOTP
from app.extensions import db
from app.forms import (
    RegisterForm, LoginForm, ChangePasswordForm,
    ForgotPasswordForm, ResetPasswordForm
)
from app.utils.otp import generate_otp
from app.utils.email import send_otp_email

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    form = RegisterForm()

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("An account with that email already exists.", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(username=form.username.data).first():
            flash("That username is already taken.", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            role=form.role.data,  # already uppercase from the form choices
        )
        db.session.add(user)
        db.session.commit()

        # Auto-create an empty profile
        profile = Profile(user_id=user.id)
        db.session.add(profile)
        db.session.commit()

        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            if not user.is_active:
                flash("Your account has been deactivated. Contact an admin.", "danger")
                return redirect(url_for("auth.login"))
            login_user(user)
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for("dashboard.home"))

        flash("Invalid email or password. Please try again.", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not check_password_hash(current_user.password, form.old_password.data):
            flash("Your current password is incorrect.", "danger")
            return redirect(url_for("auth.change_password"))

        current_user.password = generate_password_hash(form.new_password.data)
        db.session.commit()
        flash("Password updated successfully!", "success")
        return redirect(url_for("dashboard.home"))

    return render_template("auth/change_password.html", form=form)


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    form = ForgotPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            # Delete any existing OTPs for this user
            PasswordResetOTP.query.filter_by(user_id=user.id).delete()
            db.session.commit()

            otp = generate_otp()
            otp_record = PasswordResetOTP(user_id=user.id, otp=otp)
            db.session.add(otp_record)
            db.session.commit()

            # Send real email (falls back to console in dev)
            try:
                send_otp_email(user, otp)
            except Exception as e:
                current_app.logger.error(f"Email send failed: {e}")

        # Always show success to prevent email enumeration
        flash(
            "If that email exists in our system, an OTP has been sent.",
            "success"
        )
        return redirect(url_for("auth.reset_password"))

    return render_template("auth/forgot_password.html", form=form)


@auth_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            flash("Invalid email address.", "danger")
            return redirect(url_for("auth.reset_password"))

        otp_record = PasswordResetOTP.query.filter_by(
            user_id=user.id,
            otp=form.otp.data
        ).first()

        if not otp_record:
            flash("Invalid OTP. Please request a new one.", "danger")
            return redirect(url_for("auth.reset_password"))

        # Check OTP expiry
        expiry_minutes = current_app.config.get("OTP_EXPIRY_MINUTES", 10)
        if datetime.utcnow() - otp_record.created_at > timedelta(minutes=expiry_minutes):
            db.session.delete(otp_record)
            db.session.commit()
            flash(f"OTP has expired. Please request a new one.", "danger")
            return redirect(url_for("auth.forgot_password"))

        # Reset password and delete the used OTP
        user.password = generate_password_hash(form.new_password.data)
        db.session.delete(otp_record)
        db.session.commit()

        flash("Password reset successfully! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html", form=form)

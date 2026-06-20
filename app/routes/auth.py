from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.models import (
    User,
    Profile,
    PasswordResetOTP
)
from app.extensions import db

from app.forms import (
    RegisterForm,
    LoginForm,
    ChangePasswordForm,
    ForgotPasswordForm,
    ResetPasswordForm
)

from app.utils.otp import (
    generate_otp
)

auth_bp = Blueprint(
    "auth",
    __name__
)

@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        existing_user = (
            User.query.filter_by(
                email=form.email.data
            ).first()
        )

        if existing_user:

            flash(
                "Email already exists",
                "danger"
            )

            return redirect(
                url_for(
                    "auth.register"
                )
            )

        user = User(

            username=form.username.data,

            email=form.email.data,

            password=generate_password_hash(
                form.password.data
            ),

            role=form.role.data
        )

        db.session.add(user)

        db.session.commit()

        profile = Profile(
            user_id=user.id
        )

        db.session.add(profile)

        db.session.commit()

        flash(
            "Account created",
            "success"
        )

        return redirect(
            url_for(
                "auth.login"
            )
        )

    return render_template(
        "auth/register.html",
        form=form
    )

@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if (
            user
            and check_password_hash(
                user.password,
                form.password.data
            )
        ):

            login_user(user)

            return redirect(
                url_for(
                    "dashboard.home"
                )
            )

        flash(
            "Invalid credentials",
            "danger"
        )

    return render_template(
        "auth/login.html",
        form=form
    )

@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Logged out",
        "success"
    )

    return redirect(
        url_for(
            "auth.login"
        )
    )

@auth_bp.route(
    "/change-password",
    methods=["GET", "POST"]
)
@login_required
def change_password():

    form = ChangePasswordForm()

    if form.validate_on_submit():

        if not check_password_hash(
            current_user.password,
            form.old_password.data
        ):

            flash(
                "Old password incorrect",
                "danger"
            )

            return redirect(
                url_for(
                    "auth.change_password"
                )
            )

        current_user.password = (
            generate_password_hash(
                form.new_password.data
            )
        )

        db.session.commit()

        flash(
            "Password updated",
            "success"
        )

        return redirect(
            url_for(
                "dashboard.home"
            )
        )

    return render_template(
        "auth/change_password.html",
        form=form
    )

@auth_bp.route(
    "/forgot-password",
    methods=["GET", "POST"]
)
def forgot_password():

    form = ForgotPasswordForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user:

            otp = generate_otp()

            otp_record = PasswordResetOTP(

                user_id=user.id,

                otp=otp
            )

            db.session.add(
                otp_record
            )

            db.session.commit()

            print(
                f"OTP => {otp}"
            )

            flash(
                "OTP Sent",
                "success"
            )

            return redirect(
                url_for(
                    "auth.reset_password"
                )
            )

    return render_template(
        "auth/forgot_password.html",
        form=form
    )

@auth_bp.route(
    "/reset-password",
    methods=["GET", "POST"]
)
def reset_password():

    form = ResetPasswordForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        otp = PasswordResetOTP.query.filter_by(

            user_id=user.id,

            otp=form.otp.data

        ).first()

        if not otp:

            flash(
                "Invalid OTP",
                "danger"
            )

            return redirect(
                url_for(
                    "auth.reset_password"
                )
            )

        user.password = (
            generate_password_hash(
                form.new_password.data
            )
        )

        db.session.commit()

        flash(
            "Password Reset Successfully",
            "success"
        )

        return redirect(
            url_for(
                "auth.login"
            )
        )

    return render_template(
        "auth/reset_password.html",
        form=form
    )

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegisterForm(FlaskForm):
    username = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=2, max=80)]
    )
    email = EmailField(
        "Email Address",
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")]
    )
    # Uppercase values match the DB Enum and decorator checks
    role = SelectField(
        "Register As",
        choices=[("STUDENT", "Student"), ("TEACHER", "Teacher")],
        validators=[DataRequired()]
    )
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    email = EmailField(
        "Email Address",
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )
    submit = SubmitField("Sign In")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(
        "Current Password",
        validators=[DataRequired()]
    )
    new_password = PasswordField(
        "New Password",
        validators=[DataRequired(), Length(min=6)]
    )
    confirm_new_password = PasswordField(
        "Confirm New Password",
        validators=[DataRequired(), EqualTo("new_password", message="Passwords must match")]
    )
    submit = SubmitField("Change Password")


class ForgotPasswordForm(FlaskForm):
    email = EmailField(
        "Email Address",
        validators=[DataRequired(), Email()]
    )
    submit = SubmitField("Send OTP")


class ResetPasswordForm(FlaskForm):
    email = EmailField(
        "Email Address",
        validators=[DataRequired(), Email()]
    )
    otp = StringField(
        "6-Digit OTP",
        validators=[DataRequired(), Length(min=6, max=6)]
    )
    new_password = PasswordField(
        "New Password",
        validators=[DataRequired(), Length(min=6)]
    )
    confirm_new_password = PasswordField(
        "Confirm New Password",
        validators=[DataRequired(), EqualTo("new_password", message="Passwords must match")]
    )
    submit = SubmitField("Reset Password")
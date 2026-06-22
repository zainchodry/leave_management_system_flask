import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # ── Core ──────────────────────────────────────────────────
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    # ── Database ──────────────────────────────────────────────
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "leave_management.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── File Uploads ──────────────────────────────────────────
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads", "profiles")
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB

    # ── Flask-Mail (Gmail SMTP) ────────────────────────────────
    MAIL_SERVER   = os.environ.get("MAIL_SERVER",   "smtp.gmail.com")
    MAIL_PORT     = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS  = os.environ.get("MAIL_USE_TLS",  "true").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME",  "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD",  "")
    MAIL_DEFAULT_SENDER = os.environ.get(
        "MAIL_DEFAULT_SENDER",
        "EduLeave System <noreply@eduleave.com>"
    )

    # ── Login ─────────────────────────────────────────────────
    LOGIN_VIEW = "auth.login"

    # ── OTP expiry (minutes) ──────────────────────────────────
    OTP_EXPIRY_MINUTES = 10

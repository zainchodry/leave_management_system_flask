import os
from flask import Flask, render_template
from config import Config
from app.extensions import db, migrate, login_manager, mail


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ── Ensure upload folder exists ────────────────────────────
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # ── Initialise extensions ──────────────────────────────────
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"

    # ── User loader ────────────────────────────────────────────
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # ── Register blueprints ────────────────────────────────────
    from app.routes.auth        import auth_bp
    from app.routes.dashboard   import dashboard_bp
    from app.routes.leave       import leave_bp
    from app.routes.attendance  import attendance_bp
    from app.routes.departments import department_bp
    from app.routes.profile     import profile_bp
    from app.routes.notifications import notification_bp
    from app.routes.admin       import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(leave_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(department_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(admin_bp)

    # ── Custom error handlers ──────────────────────────────────
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500

    # ── Inject unread notification count into all templates ────
    @app.context_processor
    def inject_notification_count():
        from flask_login import current_user
        from app.models import Notification
        count = 0
        if current_user.is_authenticated:
            count = Notification.query.filter_by(
                receiver_id=current_user.id,
                is_read=False
            ).count()
        return {"unread_notifications": count}

    return app

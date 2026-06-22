# Student Leave Management (Flask)

A lightweight Flask application to manage student leave requests, attendance, profiles, departments, and notifications.

## Key Features

- User authentication (login, logout, password reset)
- Student profiles and departments
- Submit and review leave requests
- Attendance tracking
- Email/OTP notifications (where configured)

## Tech Stack

- Python 3.8+
- Flask
- Flask extensions (see `app/extensions.py`)
- SQLite (default) or any SQL database supported by SQLAlchemy

## Repository Structure

- [run.py](run.py) — application launcher
- [config.py](config.py) — configuration
- [app/**init**.py](app/__init__.py) — Flask app factory
- [app/extensions.py](app/extensions.py) — extension instances (db, login, migrate, etc.)
- [app/models/](app/models/) — ORM models (user, leave, attendance, profile)
- [app/forms/](app/forms/) — WTForms definitions
- [app/routes/](app/routes/) — route handlers / blueprints
- [app/utils/](app/utils/) — helper utilities (decorators, otp)

## Prerequisites

- Python 3.8 or newer
- Recommended: virtual environment

## Quickstart — Local Development

1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create environment variables

Create a `.env` file or export environment variables. Minimal recommended vars:

```bash
export FLASK_APP=run.py
export FLASK_ENV=development
export SECRET_KEY='replace-with-a-secure-secret'
# Optional: set DATABASE_URL to override default sqlite DB
export DATABASE_URL='sqlite:///student_leave.db'
```

4. Initialize the database

If this project uses Flask-Migrate:

```bash
flask db init   # only if migrations/ not present
flask db migrate -m "Initial migration"
flask db upgrade
```

If there is no migration setup, the project will create the database on first run (SQLite).

5. Run the app

```bash
flask run
# or
python run.py
```

Open http://127.0.0.1:5000 in your browser.

## Configuration

All configuration is centralized in [config.py](config.py). Common environment variables:

- `SECRET_KEY` — Flask session secret
- `DATABASE_URL` — SQLAlchemy database URI
- `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD` — for email notifications
- Any OTP or 3rd-party credentials stored in `.env` or an instance folder

Sensitive files and credentials should be kept out of source control. See [.gitignore](.gitignore).

## Creating an Admin / Seed Data

Provide a small script or use Flask shell to create initial users. Example:

```bash
flask shell
>>> from app.extensions import db
>>> from app.models.user import User
>>> u = User(email='admin@example.com', is_admin=True)
>>> u.set_password('change-me')
>>> db.session.add(u); db.session.commit()
```

## Tests

If tests are present, run them with `pytest`:

```bash
pytest
```

## Deployment Notes

- Use a production WSGI server (Gunicorn / uWSGI)
- Set `FLASK_ENV=production` and provide a strong `SECRET_KEY`
- Configure a proper production RDBMS (Postgres, MySQL) via `DATABASE_URL`
- Serve static files through a CDN or reverse proxy (nginx)

## Contributing

1. Fork the repo
2. Create a feature branch
3. Open a pull request with a clear description

Please follow the project's coding style and run tests locally.

## License

This repository does not include a license file. Add an appropriate LICENSE to clarify usage rights.

---

If you'd like, I can also:

- Add a `requirements.txt` generated from the current venv
- Add a small `docker-compose.yml` for local development
- Create initial migration scripts

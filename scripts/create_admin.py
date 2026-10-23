"""
create_admin.py
==================
Bootstraps an administrator account from ADMIN_EMAIL / ADMIN_PASSWORD /
ADMIN_NAME environment variables (see .env.example). Safe to re-run: it
will skip creation if an account with that email already exists.

Usage:
    python scripts/create_admin.py
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from APP import create_app
from APP.database import db, User


def main():
    app = create_app()
    with app.app_context():
        email = os.environ.get("ADMIN_EMAIL", "admin@interviewanalyzer.local")
        password = os.environ.get("ADMIN_PASSWORD", "ChangeMe123!")
        name = os.environ.get("ADMIN_NAME", "System Administrator")

        existing = User.query.filter_by(email=email.lower()).first()
        if existing:
            print(f"Admin account already exists for {email}.")
            return

        admin = User(full_name=name, email=email.lower(), role="admin")
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin account created: {email}")


if __name__ == "__main__":
    main()

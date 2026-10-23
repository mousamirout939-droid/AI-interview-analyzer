"""
initialize_database.py
=========================
One-off script to create all database tables. Safe to re-run (uses
create_all, which is a no-op for existing tables).

Usage:
    python scripts/initialize_database.py
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from APP import create_app
from APP.database import db


def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created/verified successfully.")


if __name__ == "__main__":
    main()

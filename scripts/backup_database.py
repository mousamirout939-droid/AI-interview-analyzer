"""
backup_database.py
=====================
Creates a timestamped copy of the SQLite database file for backup
purposes. For production Postgres/MySQL deployments, replace this with
your database provider's native backup/snapshot tooling.

Usage:
    python scripts/backup_database.py
"""

import os
import shutil
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import BASE_DIR


def main():
    db_path = os.path.join(BASE_DIR, "instance", "interview_analyzer.db")
    if not os.path.exists(db_path):
        print("No SQLite database file found to back up (are you using a different DATABASE_URL?).")
        return

    backup_dir = os.path.join(BASE_DIR, "instance", "backups")
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"interview_analyzer_{timestamp}.db")
    shutil.copy2(db_path, backup_path)
    print(f"Database backed up to: {backup_path}")


if __name__ == "__main__":
    main()

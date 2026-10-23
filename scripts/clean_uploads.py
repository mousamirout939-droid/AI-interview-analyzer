"""
clean_uploads.py
===================
Removes stale temporary files from the uploads/temp directory. Intended
to be run periodically (e.g. via cron) in production.

Usage:
    python scripts/clean_uploads.py [max_age_hours]
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from APP import create_app
from APP.utils.file_utils import clean_stale_temp_files


def main():
    max_age_hours = float(sys.argv[1]) if len(sys.argv) > 1 else 24
    app = create_app()
    with app.app_context():
        removed = clean_stale_temp_files(app.config["TEMP_FOLDER"], max_age_seconds=max_age_hours * 3600)
        print(f"Removed {removed} stale temp file(s) older than {max_age_hours}h.")


if __name__ == "__main__":
    main()

"""
file_utils.py
================
Filesystem helper utilities for saving uploads, computing file sizes, and
cleaning up temporary/orphaned files.
"""

import os
import time
import logging

logger = logging.getLogger("ai_interview_analyzer.file_utils")


def save_upload_file(file_storage, destination_path: str) -> int:
    """Save a Werkzeug FileStorage object to disk and return its size in bytes."""
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    file_storage.save(destination_path)
    return os.path.getsize(destination_path)


def get_file_size_bytes(path: str) -> int:
    return os.path.getsize(path) if os.path.exists(path) else 0


def human_readable_size(num_bytes: int) -> str:
    size = float(num_bytes)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def remove_file_if_exists(path: str) -> bool:
    if path and os.path.exists(path):
        os.remove(path)
        return True
    return False


def clean_stale_temp_files(temp_dir: str, max_age_seconds: int = 86400) -> int:
    """Delete files in temp_dir older than max_age_seconds. Returns count removed."""
    if not os.path.isdir(temp_dir):
        return 0

    removed = 0
    now = time.time()
    for name in os.listdir(temp_dir):
        path = os.path.join(temp_dir, name)
        if os.path.isfile(path) and (now - os.path.getmtime(path)) > max_age_seconds:
            os.remove(path)
            removed += 1
            logger.info("Removed stale temp file: %s", path)
    return removed

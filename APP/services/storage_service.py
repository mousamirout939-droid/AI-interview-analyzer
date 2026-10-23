"""
storage_service.py
=====================
Resolves per-interview storage paths and persists uploaded media to the
correct folder (video/original or audio/extracted), delegating to
APP.utils.file_utils / security for the low-level filesystem work.
"""

import os
from flask import current_app

from APP.utils.security import build_safe_upload_filename, base_filename_without_ext
from APP.utils.file_utils import save_upload_file


def store_uploaded_media(file_storage, file_type: str) -> dict:
    """
    Persist an uploaded file to the appropriate folder.

    Returns:
        {"stored_filename": str, "path": str, "base_filename": str, "size_bytes": int}
    """
    stored_filename = build_safe_upload_filename(file_storage.filename, prefix="interview")
    base_filename = base_filename_without_ext(stored_filename)

    target_dir = (
        current_app.config["VIDEO_ORIGINAL_FOLDER"]
        if file_type == "video"
        else current_app.config["AUDIO_EXTRACTED_FOLDER"]
    )
    destination = os.path.join(target_dir, stored_filename)
    size_bytes = save_upload_file(file_storage, destination)

    return {
        "stored_filename": stored_filename,
        "path": destination,
        "base_filename": base_filename,
        "size_bytes": size_bytes,
    }

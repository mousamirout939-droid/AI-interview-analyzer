"""
upload.py (middleware)
=========================
Pre-flight validation for file uploads: extension whitelist and size
checks applied before the file is persisted to disk or handed to the AI
pipeline.
"""

from APP.utils.validators import is_allowed_file


class UploadValidationError(Exception):
    pass


def validate_upload(file_storage, allowed_video_ext: set, allowed_audio_ext: set, max_bytes: int):
    if file_storage is None or file_storage.filename == "":
        raise UploadValidationError("No file was selected for upload.")

    allowed = allowed_video_ext | allowed_audio_ext
    if not is_allowed_file(file_storage.filename, allowed):
        raise UploadValidationError(
            f"Unsupported file type. Allowed types: {', '.join(sorted(allowed))}."
        )

    file_storage.stream.seek(0, 2)  # seek to end
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)

    if size > max_bytes:
        max_mb = max_bytes / (1024 * 1024)
        raise UploadValidationError(f"File exceeds the maximum allowed size of {max_mb:.0f}MB.")

    ext = file_storage.filename.rsplit(".", 1)[1].lower()
    file_type = "video" if ext in allowed_video_ext else "audio"
    return file_type, size

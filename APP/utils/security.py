"""
security.py
==============
Security helper utilities: secure random token generation (password reset,
CSRF-adjacent use cases) and filename sanitization to prevent path
traversal on upload.
"""

import os
import secrets
import time
from werkzeug.utils import secure_filename


def generate_secure_token(num_bytes: int = 32) -> str:
    return secrets.token_urlsafe(num_bytes)


def build_safe_upload_filename(original_filename: str, prefix: str = "interview") -> str:
    """
    Build a collision-resistant, path-safe filename for stored uploads:
    <prefix>_<unix_timestamp>_<random_hex>.<ext>
    """
    safe_name = secure_filename(original_filename)
    ext = safe_name.rsplit(".", 1)[1].lower() if "." in safe_name else "bin"
    unique_part = f"{int(time.time())}_{secrets.token_hex(4)}"
    return f"{prefix}_{unique_part}.{ext}"


def base_filename_without_ext(filename: str) -> str:
    return os.path.splitext(filename)[0]

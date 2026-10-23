"""
validators.py
================
Input validation helpers for auth forms and upload requests. Kept
dependency-light (no external validation framework) for transparency and
easy unit testing.
"""

import re

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email: str) -> bool:
    return bool(email) and bool(_EMAIL_RE.match(email.strip()))


def is_valid_password(password: str, min_length: int = 8) -> tuple:
    """
    Returns (is_valid: bool, message: str).
    Requires: minimum length, at least one letter and one digit.
    """
    if not password or len(password) < min_length:
        return False, f"Password must be at least {min_length} characters long."
    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain at least one letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    return True, "OK"


def is_valid_name(name: str) -> bool:
    return bool(name) and 2 <= len(name.strip()) <= 150


def is_allowed_file(filename: str, allowed_extensions: set) -> bool:
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in allowed_extensions

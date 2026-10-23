"""
auth.py (middleware)
=======================
Route-protection decorators layered on top of Flask-Login: role-based
access control for admin-only views, plus an ownership check helper so
candidates can only access their own interview records.
"""

from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user


def admin_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))
        if not current_user.is_admin:
            abort(403)
        return view_func(*args, **kwargs)
    return wrapped


def owns_interview_or_admin(interview) -> bool:
    """Return True if current_user owns the given interview or is an admin."""
    if not current_user.is_authenticated:
        return False
    return current_user.is_admin or interview.user_id == current_user.id

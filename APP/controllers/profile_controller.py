"""
profile_controller.py
========================
Handles viewing and updating the current user's profile (name, bio).
Email/password changes are intentionally kept out of this simple form to
avoid the added complexity of re-verification flows in this MVP.
"""

import logging
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from APP.database import db
from APP.utils.validators import is_valid_name

logger = logging.getLogger("ai_interview_analyzer.profile_controller")


@login_required
def view_profile():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        bio = request.form.get("bio", "").strip()

        if not is_valid_name(full_name):
            flash("Please enter a valid name.", "error")
        else:
            current_user.full_name = full_name
            current_user.bio = bio
            db.session.commit()
            flash("Profile updated successfully.", "success")
        return redirect(url_for("profile.view_profile"))

    return render_template("profile.html")

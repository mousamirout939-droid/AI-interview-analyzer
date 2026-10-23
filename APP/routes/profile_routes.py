"""
profile_routes.py
====================
Blueprint for viewing/updating the current user's profile.
"""

from flask import Blueprint
from APP.controllers.profile_controller import view_profile

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")

profile_bp.add_url_rule("/", view_func=view_profile, methods=["GET", "POST"])

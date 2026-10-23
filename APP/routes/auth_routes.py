"""
auth_routes.py
=================
Blueprint for registration, login, and logout endpoints.
"""

from flask import Blueprint
from APP.controllers.auth_controller import handle_register, handle_login, handle_logout

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

auth_bp.add_url_rule("/register", endpoint="register", view_func=handle_register, methods=["GET", "POST"])
auth_bp.add_url_rule("/login", endpoint="login", view_func=handle_login, methods=["GET", "POST"])
auth_bp.add_url_rule("/logout", endpoint="logout", view_func=handle_logout, methods=["GET"])

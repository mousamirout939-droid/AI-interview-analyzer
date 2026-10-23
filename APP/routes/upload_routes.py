"""
upload_routes.py
===================
Blueprint for the interview upload form/endpoint.
"""

from flask import Blueprint
from APP.controllers.upload_controller import handle_upload

upload_bp = Blueprint("upload", __name__, url_prefix="/upload")

upload_bp.add_url_rule("/", view_func=handle_upload, methods=["GET", "POST"])

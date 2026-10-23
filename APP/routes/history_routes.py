"""
history_routes.py
====================
Blueprint for the interview history/listing view.
"""

from flask import Blueprint
from APP.controllers.history_controller import view_history

history_bp = Blueprint("history", __name__, url_prefix="/history")

history_bp.add_url_rule("/", view_func=view_history, methods=["GET"])

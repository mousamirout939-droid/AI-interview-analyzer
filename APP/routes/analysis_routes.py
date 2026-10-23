"""
analysis_routes.py
=====================
Blueprint for viewing a single interview's detailed analysis.
"""

from flask import Blueprint
from APP.controllers.analysis_controller import view_analysis

analysis_bp = Blueprint("analysis", __name__, url_prefix="/analysis")

analysis_bp.add_url_rule("/<int:interview_id>", view_func=view_analysis, methods=["GET"])

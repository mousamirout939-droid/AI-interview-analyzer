"""
report_routes.py
===================
Blueprint for the HTML report view and PDF download endpoint.
"""

from flask import Blueprint
from APP.controllers.report_controller import view_report, download_report_pdf

report_bp = Blueprint("report", __name__, url_prefix="/report")

report_bp.add_url_rule("/<int:interview_id>", view_func=view_report, methods=["GET"])
report_bp.add_url_rule("/<int:interview_id>/download", view_func=download_report_pdf, methods=["GET"])

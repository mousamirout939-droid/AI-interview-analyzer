"""
report_controller.py
=======================
Serves the printable HTML report view and the downloadable PDF export for
a completed interview.
"""

import logging
from flask import render_template, abort, send_file, current_app
from flask_login import login_required

from APP.database import Interview
from APP.middleware.auth import owns_interview_or_admin
from APP.services.report_service import get_report_bundle, generate_pdf_report

logger = logging.getLogger("ai_interview_analyzer.report_controller")


@login_required
def view_report(interview_id: int):
    interview = Interview.query.get_or_404(interview_id)
    if not owns_interview_or_admin(interview):
        abort(403)

    bundle = get_report_bundle(interview_id)
    return render_template("report.html", **bundle)


@login_required
def download_report_pdf(interview_id: int):
    interview = Interview.query.get_or_404(interview_id)
    if not owns_interview_or_admin(interview):
        abort(403)

    try:
        pdf_path = generate_pdf_report(interview_id, output_dir=current_app.config["REPORT_FOLDER"])
    except ValueError as exc:
        abort(404, description=str(exc))

    return send_file(pdf_path, as_attachment=True, download_name=f"interview_{interview_id}_report.pdf")

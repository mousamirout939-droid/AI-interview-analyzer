"""
analysis_controller.py
=========================
Renders the detailed analysis view for a single interview: dimension
scores, sentiment breakdown, transcript, strengths/weaknesses, and tips.
"""

import json
import logging
from flask import render_template, abort
from flask_login import login_required, current_user

from APP.database import Interview, Analysis, Report, Transcript
from APP.middleware.auth import owns_interview_or_admin

logger = logging.getLogger("ai_interview_analyzer.analysis_controller")


@login_required
def view_analysis(interview_id: int):
    interview = Interview.query.get_or_404(interview_id)
    if not owns_interview_or_admin(interview):
        abort(403)

    analysis = Analysis.query.filter_by(interview_id=interview_id).first()
    report = Report.query.filter_by(interview_id=interview_id).first()
    transcript = Transcript.query.filter_by(interview_id=interview_id).first()

    strengths = json.loads(report.strengths_json) if report and report.strengths_json else []
    weaknesses = json.loads(report.weaknesses_json) if report and report.weaknesses_json else []
    tips = json.loads(report.tips_json) if report and report.tips_json else []

    return render_template(
        "analysis.html",
        interview=interview,
        analysis=analysis,
        report=report,
        transcript=transcript,
        strengths=strengths,
        weaknesses=weaknesses,
        tips=tips,
    )

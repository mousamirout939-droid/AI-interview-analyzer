"""Resume-based study roadmap and interview preparation."""

from flask import Blueprint, render_template, request
from flask_login import login_required

from APP.services.resume_coach_service import (
    ResumeAnalysisError,
    analyze_resume,
    extract_resume_text,
)

resume_bp = Blueprint("resume", __name__, url_prefix="/resume")


@resume_bp.route("/", methods=["GET", "POST"])
@login_required
def roadmap():
    if request.method == "GET":
        return render_template("resume_coach.html")

    resume_file = request.files.get("resume_file")
    target_role = request.form.get("target_role", "auto")

    try:
        resume_text = extract_resume_text(resume_file)
        result = analyze_resume(resume_text, target_role)
    except ResumeAnalysisError as exc:
        return render_template("resume_coach.html", error=str(exc)), 400

    return render_template("resume_coach.html", result=result)

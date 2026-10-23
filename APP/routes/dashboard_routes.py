"""
dashboard_routes.py
======================
Blueprint for the authenticated user's dashboard (overview stats + recent
interviews).
"""

from flask import Blueprint, render_template
from flask_login import login_required, current_user

from APP.database import Interview, Analysis
from sqlalchemy import func
from APP.database import db

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
@login_required
def index():
    base_query = Interview.query if current_user.is_admin else Interview.query.filter_by(user_id=current_user.id)

    total_interviews = base_query.count()
    completed_interviews = base_query.filter_by(status="completed").count()
    recent_interviews = base_query.order_by(Interview.created_at.desc()).limit(5).all()

    avg_score_query = (
        db.session.query(func.avg(Analysis.overall_score))
        .join(Interview, Analysis.interview_id == Interview.id)
    )
    if not current_user.is_admin:
        avg_score_query = avg_score_query.filter(Interview.user_id == current_user.id)
    avg_score = avg_score_query.scalar()

    return render_template(
        "dashboard.html",
        total_interviews=total_interviews,
        completed_interviews=completed_interviews,
        recent_interviews=recent_interviews,
        avg_score=round(avg_score, 1) if avg_score else None,
    )

"""
ranking_controller.py
========================
Renders the candidate leaderboard/ranking view.
"""

import logging
from flask import render_template
from flask_login import login_required

from APP.services.ranking_service import get_leaderboard

logger = logging.getLogger("ai_interview_analyzer.ranking_controller")


@login_required
def view_ranking():
    leaderboard = get_leaderboard(limit=100)
    return render_template("ranking.html", leaderboard=leaderboard)

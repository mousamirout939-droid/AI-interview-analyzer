"""
ranking_routes.py
====================
Blueprint for the candidate leaderboard/ranking view.
"""

from flask import Blueprint
from APP.controllers.ranking_controller import view_ranking

ranking_bp = Blueprint("ranking", __name__, url_prefix="/ranking")

ranking_bp.add_url_rule("/", view_func=view_ranking, methods=["GET"])

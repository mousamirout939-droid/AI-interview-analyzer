"""
ranking_service.py
=====================
Recomputes and persists the candidate leaderboard by reading all
completed Analysis rows, delegating rank computation to
AI.scoring.candidate_ranker, and upserting Ranking rows.
"""

from APP.database import db, Analysis, Interview, User, Ranking
from AI.scoring.candidate_ranker import rank_candidates


def refresh_rankings() -> list:
    """
    Recompute rankings across all completed interviews and persist them.
    Returns the freshly ranked list of candidate dicts.
    """
    rows = (
        db.session.query(Analysis, Interview, User)
        .join(Interview, Analysis.interview_id == Interview.id)
        .join(User, Interview.user_id == User.id)
        .filter(Interview.status == "completed")
        .all()
    )

    candidates = [
        {
            "interview_id": interview.id,
            "user_id": user.id,
            "name": user.full_name,
            "title": interview.title,
            "overall_score": analysis.overall_score,
            "verdict": analysis.verdict,
        }
        for analysis, interview, user in rows
    ]

    ranked = rank_candidates(candidates)

    for candidate in ranked:
        ranking = Ranking.query.filter_by(interview_id=candidate["interview_id"]).first()
        if ranking is None:
            ranking = Ranking(interview_id=candidate["interview_id"], user_id=candidate["user_id"])
            db.session.add(ranking)
        ranking.overall_score = candidate["overall_score"]
        ranking.rank_position = candidate["rank"]
        ranking.percentile = candidate["percentile"]

    db.session.commit()
    return ranked


def get_leaderboard(limit: int = 50) -> list:
    ranked = refresh_rankings()
    return ranked[:limit]

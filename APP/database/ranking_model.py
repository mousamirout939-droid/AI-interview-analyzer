"""
ranking_model.py
===================
Materialized ranking snapshot rows, refreshed periodically by
ranking_service.py, so the leaderboard can be served without recomputing
ranks across all interviews on every page load.
"""

from datetime import datetime, timezone
from APP.database.database import db


class Ranking(db.Model):
    __tablename__ = "rankings"

    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id"), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    overall_score = db.Column(db.Float, nullable=False, default=0.0)
    rank_position = db.Column(db.Integer, nullable=True, index=True)
    percentile = db.Column(db.Float, nullable=True)

    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                            onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        return {
            "interview_id": self.interview_id,
            "user_id": self.user_id,
            "overall_score": self.overall_score,
            "rank_position": self.rank_position,
            "percentile": self.percentile,
        }

    def __repr__(self):
        return f"<Ranking interview={self.interview_id} rank={self.rank_position}>"

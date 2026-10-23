"""
analysis_model.py
====================
Stores the six dimension scores plus overall score and sentiment summary
for a given interview. This is the numeric core the dashboard, report,
and ranking views all read from.
"""

from datetime import datetime, timezone
from APP.database.database import db


class Analysis(db.Model):
    __tablename__ = "analyses"

    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id"), nullable=False, unique=True)

    fluency_score = db.Column(db.Float, nullable=False, default=0.0)
    confidence_score = db.Column(db.Float, nullable=False, default=0.0)
    grammar_score = db.Column(db.Float, nullable=False, default=0.0)
    vocabulary_score = db.Column(db.Float, nullable=False, default=0.0)
    technical_score = db.Column(db.Float, nullable=False, default=0.0)
    communication_score = db.Column(db.Float, nullable=False, default=0.0)
    overall_score = db.Column(db.Float, nullable=False, default=0.0, index=True)
    verdict = db.Column(db.String(30), nullable=True)

    sentiment_label = db.Column(db.String(20), nullable=True)
    sentiment_polarity = db.Column(db.Float, nullable=True)
    dominant_emotion = db.Column(db.String(30), nullable=True)

    word_count = db.Column(db.Integer, nullable=True)
    filler_word_count = db.Column(db.Integer, nullable=True)

    raw_summary_json = db.Column(db.Text, nullable=True)  # full pipeline summary, JSON-encoded

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def dimension_scores(self) -> dict:
        return {
            "fluency": self.fluency_score,
            "confidence": self.confidence_score,
            "grammar": self.grammar_score,
            "vocabulary": self.vocabulary_score,
            "technical": self.technical_score,
            "communication": self.communication_score,
        }

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "interview_id": self.interview_id,
            **self.dimension_scores(),
            "overall_score": self.overall_score,
            "verdict": self.verdict,
            "sentiment_label": self.sentiment_label,
            "sentiment_polarity": self.sentiment_polarity,
            "dominant_emotion": self.dominant_emotion,
            "word_count": self.word_count,
            "filler_word_count": self.filler_word_count,
        }

    def __repr__(self):
        return f"<Analysis interview={self.interview_id} overall={self.overall_score}>"

"""
report_model.py
==================
Stores metadata about a generated PDF/HTML report artifact (feedback
narrative, strengths, weaknesses, tips, and the path to the exported PDF).
"""

from datetime import datetime, timezone
from APP.database.database import db


class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id"), nullable=False, unique=True)

    feedback_text = db.Column(db.Text, nullable=True)
    strengths_json = db.Column(db.Text, nullable=True)
    weaknesses_json = db.Column(db.Text, nullable=True)
    tips_json = db.Column(db.Text, nullable=True)

    pdf_path = db.Column(db.String(255), nullable=True)
    generated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "interview_id": self.interview_id,
            "feedback_text": self.feedback_text,
            "pdf_path": self.pdf_path,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }

    def __repr__(self):
        return f"<Report interview={self.interview_id}>"

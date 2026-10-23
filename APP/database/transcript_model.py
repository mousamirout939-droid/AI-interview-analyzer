"""
transcript_model.py
======================
Stores the raw and cleaned transcript text produced by the speech-to-text
stage, plus a pointer to the structured JSON artifact on disk.
"""

from datetime import datetime, timezone
from APP.database.database import db


class Transcript(db.Model):
    __tablename__ = "transcripts"

    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id"), nullable=False, unique=True)

    raw_text = db.Column(db.Text, nullable=True)
    cleaned_text = db.Column(db.Text, nullable=True)
    language_code = db.Column(db.String(10), nullable=True, default="en")
    language_confidence = db.Column(db.Float, nullable=True)
    transcription_engine = db.Column(db.String(30), nullable=True)

    raw_path = db.Column(db.String(255), nullable=True)
    cleaned_path = db.Column(db.String(255), nullable=True)
    json_path = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "interview_id": self.interview_id,
            "raw_text": self.raw_text,
            "cleaned_text": self.cleaned_text,
            "language_code": self.language_code,
            "transcription_engine": self.transcription_engine,
        }

    def __repr__(self):
        return f"<Transcript for interview {self.interview_id}>"

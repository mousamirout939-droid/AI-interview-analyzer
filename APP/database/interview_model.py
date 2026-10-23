"""
interview_model.py
=====================
Represents a single uploaded interview session (video/audio + metadata).
Acts as the anchor record that Transcript, Analysis, and Report rows
attach to via foreign key.
"""

from datetime import datetime, timezone
from APP.database.database import db


class Interview(db.Model):
    __tablename__ = "interviews"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    title = db.Column(db.String(200), nullable=False, default="Untitled Interview")
    question = db.Column(db.Text, nullable=True)

    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(10), nullable=False, default="video")  # video | audio
    file_size_bytes = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Float, nullable=True)
    thumbnail_path = db.Column(db.String(255), nullable=True)

    status = db.Column(db.String(20), nullable=False, default="uploaded")
    # uploaded -> processing -> completed -> failed
    error_message = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    processed_at = db.Column(db.DateTime, nullable=True)

    transcript = db.relationship("Transcript", backref="interview", uselist=False,
                                  cascade="all, delete-orphan")
    analysis = db.relationship("Analysis", backref="interview", uselist=False,
                                cascade="all, delete-orphan")
    report = db.relationship("Report", backref="interview", uselist=False,
                              cascade="all, delete-orphan")

    def stored_path(self) -> str:
        """Resolve the absolute filesystem path of the originally uploaded media file."""
        from flask import current_app
        import os
        folder = (
            current_app.config["VIDEO_ORIGINAL_FOLDER"]
            if self.file_type == "video"
            else current_app.config["AUDIO_EXTRACTED_FOLDER"]
        )
        return os.path.join(folder, self.stored_filename)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "question": self.question,
            "file_type": self.file_type,
            "status": self.status,
            "duration_seconds": self.duration_seconds,
            "thumbnail_path": self.thumbnail_path,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
        }

    def __repr__(self):
        return f"<Interview {self.id} - {self.title} ({self.status})>"

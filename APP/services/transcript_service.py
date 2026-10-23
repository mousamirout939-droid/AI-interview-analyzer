"""
transcript_service.py
========================
Read-side helper for fetching transcript content/metadata for an
interview, used by the analysis and report controllers.
"""

from APP.database import Transcript


def get_transcript_for_interview(interview_id: int) -> Transcript:
    return Transcript.query.filter_by(interview_id=interview_id).first()

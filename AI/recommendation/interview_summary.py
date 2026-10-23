"""
interview_summary.py
======================
Assembles the final structured summary object combining transcript stats,
sentiment, all dimension scores, overall score, strengths, weaknesses,
tips, and narrative feedback. This is the object persisted as an
Analysis/Report record and rendered in the UI.
"""

from datetime import datetime, timezone


def build_interview_summary(transcript_stats: dict, sentiment: dict, scores: dict,
                             overall: dict, strengths: list, weaknesses: list,
                             tips: list, feedback: str) -> dict:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "transcript_stats": transcript_stats,
        "sentiment": sentiment,
        "dimension_scores": scores,
        "overall": overall,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "improvement_tips": tips,
        "feedback": feedback,
    }

"""
helpers.py
============
Miscellaneous small helpers shared across controllers/templates: date
formatting, score-to-color mapping (for the themed UI), and pagination.
"""

from datetime import datetime


def format_datetime(value, fmt: str = "%b %d, %Y %I:%M %p") -> str:
    if value is None:
        return "—"
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except ValueError:
            return value
    return value.strftime(fmt)


def score_badge_class(score: float) -> str:
    """Map a 0-100 score to a themed CSS badge class name."""
    if score >= 85:
        return "badge-excellent"   # green
    if score >= 70:
        return "badge-strong"      # lavender
    if score >= 55:
        return "badge-satisfactory"  # pink
    return "badge-needs-work"      # muted red


def truncate_text(text: str, max_length: int = 160) -> str:
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[: max_length - 1].rstrip() + "…"


def seconds_to_mmss(seconds: float) -> str:
    if seconds is None:
        return "0:00"
    total = int(seconds)
    minutes, secs = divmod(total, 60)
    return f"{minutes}:{secs:02d}"

"""
language_detector.py
======================
Detects the spoken/written language of a transcript so downstream NLP
components can decide whether to proceed (this pipeline is tuned for
English) or flag the interview for manual review.
"""

import logging
from textblob import TextBlob

logger = logging.getLogger("ai_interview_analyzer.language_detector")

# Common English function words used as a lightweight fallback detector
# when no network-dependent language API is available.
_ENGLISH_MARKERS = {
    "the", "and", "is", "was", "i", "to", "a", "of", "in", "that", "it",
    "for", "on", "with", "as", "this", "my", "we", "have", "are",
}


def detect_language(text: str) -> dict:
    """
    Detect the language of the given text.

    Returns a dict: {"language": "en", "confidence": 0.92, "is_english": True}

    Uses a simple, dependency-free heuristic (function-word overlap) so the
    system works fully offline. This can be swapped for a proper language
    ID model (e.g. langdetect, fastText lid.176) in production.
    """
    if not text or not text.strip():
        return {"language": "unknown", "confidence": 0.0, "is_english": False}

    words = [w.strip(".,!?;:").lower() for w in text.split()]
    if not words:
        return {"language": "unknown", "confidence": 0.0, "is_english": False}

    matches = sum(1 for w in words if w in _ENGLISH_MARKERS)
    ratio = matches / len(words)
    confidence = min(1.0, round(ratio * 4, 2))  # scale heuristic into 0-1 range
    is_english = ratio > 0.05 or len(words) < 5

    return {
        "language": "en" if is_english else "unknown",
        "confidence": confidence,
        "is_english": is_english,
    }

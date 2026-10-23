"""
emotion_analysis.py
=====================
Lightweight, lexicon-based emotion classification (confidence, nervousness,
enthusiasm, calmness) derived from sentiment polarity/subjectivity plus
keyword cues. This is not a deep-learning emotion classifier; it's a
transparent, explainable heuristic well-suited to generating interpretable
interview feedback.
"""

import re

from AI.sentiment.polarity_score import compute_polarity
from AI.sentiment.subjectivity_score import compute_subjectivity

_CONFIDENCE_CUES = [
    "i am confident", "i believe", "i successfully", "i led", "i achieved",
    "i am certain", "i know", "definitely", "certainly", "i managed",
]
_NERVOUSNESS_CUES = [
    "i'm not sure", "i am not sure", "maybe", "i guess", "i think maybe",
    "i don't know", "i'm nervous", "sorry", "um", "uh",
]
_ENTHUSIASM_CUES = [
    "excited", "passionate", "love", "enjoy", "great opportunity", "thrilled",
]


def _count_cues(text_lower: str, cues: list) -> int:
    return sum(1 for cue in cues if cue in text_lower)


def analyze_emotion(text: str) -> dict:
    """
    Returns a dict of normalized (0-1) scores for each emotional dimension
    plus a single dominant_emotion label.
    """
    if not text or not text.strip():
        return {
            "confidence": 0.5, "nervousness": 0.5, "enthusiasm": 0.5, "calmness": 0.5,
            "dominant_emotion": "neutral",
        }

    text_lower = text.lower()
    polarity_info = compute_polarity(text)
    subjectivity_info = compute_subjectivity(text)

    confidence_hits = _count_cues(text_lower, _CONFIDENCE_CUES)
    nervousness_hits = _count_cues(text_lower, _NERVOUSNESS_CUES)
    enthusiasm_hits = _count_cues(text_lower, _ENTHUSIASM_CUES)

    word_count = max(1, len(text_lower.split()))

    confidence = min(1.0, 0.5 + polarity_info["polarity"] * 0.3 + (confidence_hits / word_count) * 10)
    nervousness = min(1.0, 0.3 + (nervousness_hits / word_count) * 15 - polarity_info["polarity"] * 0.2)
    enthusiasm = min(1.0, 0.4 + (enthusiasm_hits / word_count) * 12 + polarity_info["polarity"] * 0.3)
    calmness = min(1.0, 1.0 - nervousness * 0.8 + (1 - subjectivity_info["subjectivity"]) * 0.2)

    scores = {
        "confidence": round(max(0.0, confidence), 3),
        "nervousness": round(max(0.0, nervousness), 3),
        "enthusiasm": round(max(0.0, enthusiasm), 3),
        "calmness": round(max(0.0, calmness), 3),
    }
    dominant = max(scores, key=scores.get)
    scores["dominant_emotion"] = dominant
    return scores

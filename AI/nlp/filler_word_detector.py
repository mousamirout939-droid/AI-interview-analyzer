"""
filler_word_detector.py
=========================
Detects filler words / verbal hesitations ("um", "uh", "like", "you know",
etc.) in a transcript. Filler word frequency is a strong, well-established
proxy for speaking confidence and fluency in interview analysis.
"""

import os
import re
import functools

_FILLER_WORDS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "datasets", "filler_words.txt")


@functools.lru_cache(maxsize=1)
def _load_filler_words() -> list:
    path = os.path.abspath(_FILLER_WORDS_PATH)
    if not os.path.exists(path):
        return ["um", "uh", "like", "you know", "i mean", "actually", "basically"]
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]


def detect_filler_words(text: str) -> dict:
    """
    Count occurrences of each filler phrase in the transcript.

    Returns:
        {
            "total_fillers": int,
            "filler_breakdown": {"um": 3, "like": 2, ...},
            "filler_rate_per_100_words": float
        }
    """
    if not text:
        return {"total_fillers": 0, "filler_breakdown": {}, "filler_rate_per_100_words": 0.0}

    lower_text = text.lower()
    word_count = max(1, len(lower_text.split()))
    breakdown = {}

    for phrase in _load_filler_words():
        pattern = r"\b" + re.escape(phrase) + r"\b"
        matches = re.findall(pattern, lower_text)
        if matches:
            breakdown[phrase] = len(matches)

    total = sum(breakdown.values())
    rate = round((total / word_count) * 100, 2)

    return {
        "total_fillers": total,
        "filler_breakdown": breakdown,
        "filler_rate_per_100_words": rate,
    }

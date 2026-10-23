"""
subjectivity_score.py
=======================
Computes subjectivity (0.0 fully objective / factual to 1.0 fully
subjective / opinion-based) for a transcript using TextBlob. Interview
answers with a healthy balance (moderate subjectivity) tend to combine
factual evidence with personal reflection, which is generally desirable.
"""

from textblob import TextBlob


def compute_subjectivity(text: str) -> dict:
    if not text or not text.strip():
        return {"subjectivity": 0.0, "label": "objective"}

    blob = TextBlob(text)
    subjectivity = round(blob.sentiment.subjectivity, 3)

    if subjectivity < 0.35:
        label = "objective"
    elif subjectivity < 0.65:
        label = "balanced"
    else:
        label = "subjective"

    return {"subjectivity": subjectivity, "label": label}

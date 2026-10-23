"""
sentiment_analysis.py
=======================
High-level orchestrator that combines polarity, subjectivity, and emotion
analysis into a single sentiment report for a transcript. This is the
public entry point used by the scoring pipeline.
"""

from AI.sentiment.polarity_score import compute_polarity
from AI.sentiment.subjectivity_score import compute_subjectivity
from AI.sentiment.emotion_analysis import analyze_emotion


def analyze_sentiment(text: str) -> dict:
    """
    Returns a combined sentiment report:
        {
            "polarity": {...},
            "subjectivity": {...},
            "emotion": {...},
            "overall_tone": "positive" | "neutral" | "negative"
        }
    """
    polarity = compute_polarity(text)
    subjectivity = compute_subjectivity(text)
    emotion = analyze_emotion(text)

    return {
        "polarity": polarity,
        "subjectivity": subjectivity,
        "emotion": emotion,
        "overall_tone": polarity["label"],
    }

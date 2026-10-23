"""
test_sentiment.py
====================
Unit tests for the sentiment/emotion analysis layer.
"""

from AI.sentiment.polarity_score import compute_polarity
from AI.sentiment.subjectivity_score import compute_subjectivity
from AI.sentiment.emotion_analysis import analyze_emotion
from AI.sentiment.sentiment_analysis import analyze_sentiment


def test_positive_polarity():
    result = compute_polarity("I am extremely confident, excited, and proud of what I achieved.")
    assert result["polarity"] > 0
    assert result["label"] == "positive"


def test_negative_polarity():
    result = compute_polarity("I really struggled and made a lot of mistakes, it was a poor result.")
    assert result["polarity"] < 0
    assert result["label"] == "negative"


def test_subjectivity_range():
    result = compute_subjectivity("The system processed one million requests per second.")
    assert 0.0 <= result["subjectivity"] <= 1.0


def test_emotion_analysis_returns_dominant():
    result = analyze_emotion("I am confident and excited about this achievement.")
    assert "dominant_emotion" in result
    assert 0.0 <= result["confidence"] <= 1.0


def test_full_sentiment_analysis():
    result = analyze_sentiment("I successfully led the project and I am proud of the outcome.")
    assert "polarity" in result and "subjectivity" in result and "emotion" in result
    assert result["overall_tone"] in {"positive", "neutral", "negative"}

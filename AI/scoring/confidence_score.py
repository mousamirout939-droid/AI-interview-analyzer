"""
confidence_score.py
=====================
Scores perceived confidence (0-100) using the emotion-analysis dimensions
(confidence, nervousness, calmness) plus filler-word rate as a
corroborating signal.
"""

def calculate_confidence_score(emotion_scores: dict, filler_stats: dict) -> dict:
    """
    Args:
        emotion_scores: output of AI.sentiment.emotion_analysis.analyze_emotion
        filler_stats: output of AI.nlp.filler_word_detector.detect_filler_words

    Returns:
        {"score": float 0-100, "breakdown": {...}}
    """
    confidence = emotion_scores.get("confidence", 0.5)
    nervousness = emotion_scores.get("nervousness", 0.5)
    calmness = emotion_scores.get("calmness", 0.5)
    filler_rate = filler_stats.get("filler_rate_per_100_words", 0.0)

    filler_penalty = min(0.3, filler_rate / 100)

    raw = (confidence * 0.45) + (calmness * 0.35) + ((1 - nervousness) * 0.20) - filler_penalty
    score = max(0.0, min(1.0, raw)) * 100

    return {
        "score": round(score, 1),
        "breakdown": {
            "confidence_signal": confidence,
            "calmness_signal": calmness,
            "nervousness_signal": nervousness,
            "filler_penalty": round(filler_penalty, 3),
        },
    }

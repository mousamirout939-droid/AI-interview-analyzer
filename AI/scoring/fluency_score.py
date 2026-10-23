"""
fluency_score.py
==================
Scores speaking fluency (0-100) from filler-word frequency, pause
statistics, and speaking rate.
"""

def calculate_fluency_score(filler_stats: dict, pause_stats: dict, word_count: int, duration_seconds: float) -> dict:
    """
    Args:
        filler_stats: output of AI.nlp.filler_word_detector.detect_filler_words
        pause_stats: output of AI.speech.silence_detection.compute_pause_statistics
        word_count: total words spoken
        duration_seconds: total audio duration in seconds

    Returns:
        {"score": float 0-100, "breakdown": {...}}
    """
    filler_rate = filler_stats.get("filler_rate_per_100_words", 0.0)
    speaking_ratio = pause_stats.get("speaking_ratio", 0.8) if pause_stats else 0.8
    avg_pause_ms = pause_stats.get("avg_pause_ms", 0) if pause_stats else 0

    words_per_minute = (word_count / (duration_seconds / 60)) if duration_seconds and duration_seconds > 0 else 120

    # Ideal speaking pace for interviews: ~110-160 WPM
    if 110 <= words_per_minute <= 160:
        pace_score = 100
    else:
        distance = min(abs(words_per_minute - 110), abs(words_per_minute - 160)) if words_per_minute < 110 or words_per_minute > 160 else 0
        pace_score = max(0, 100 - distance * 1.2)

    filler_penalty = min(40, filler_rate * 4)  # heavier filler use drags score down
    pause_penalty = min(20, (avg_pause_ms / 1000) * 5) if avg_pause_ms else 0
    speaking_ratio_bonus = speaking_ratio * 20

    raw_score = (pace_score * 0.5) + (speaking_ratio_bonus) + (30 - filler_penalty) - pause_penalty
    score = max(0.0, min(100.0, raw_score))

    return {
        "score": round(score, 1),
        "breakdown": {
            "words_per_minute": round(words_per_minute, 1),
            "pace_score": round(pace_score, 1),
            "filler_rate_per_100_words": filler_rate,
            "speaking_ratio": speaking_ratio,
            "avg_pause_ms": avg_pause_ms,
        },
    }

"""
overall_score.py
==================
Combines all individual dimension scores into a single weighted overall
interview score (0-100), plus a letter-grade style verdict.
"""

DEFAULT_WEIGHTS = {
    "fluency": 0.20,
    "confidence": 0.20,
    "grammar": 0.15,
    "vocabulary": 0.15,
    "technical": 0.15,
    "communication": 0.15,
}


def calculate_overall_score(scores: dict, weights: dict = None) -> dict:
    """
    Args:
        scores: dict mapping dimension name -> numeric score (0-100), e.g.
                {"fluency": 82.0, "confidence": 75.5, "grammar": 90.0,
                 "vocabulary": 68.0, "technical": 60.0, "communication": 77.0}
        weights: optional custom weight dict (must sum to ~1.0)

    Returns:
        {"overall_score": float, "verdict": str, "weights_used": dict}
    """
    weights = weights or DEFAULT_WEIGHTS
    total_weight = sum(weights.get(dim, 0) for dim in scores) or 1.0

    weighted_sum = sum(scores.get(dim, 0) * weights.get(dim, 0) for dim in scores)
    overall = weighted_sum / total_weight

    verdict = _verdict_for_score(overall)

    return {
        "overall_score": round(overall, 1),
        "verdict": verdict,
        "weights_used": weights,
    }


def _verdict_for_score(score: float) -> str:
    if score >= 85:
        return "Excellent"
    if score >= 70:
        return "Strong"
    if score >= 55:
        return "Satisfactory"
    if score >= 40:
        return "Needs Improvement"
    return "Poor"

"""
strengths_detector.py
=======================
Identifies a candidate's top strengths from their dimension scores, so
feedback can highlight what to keep doing well.
"""

_STRENGTH_LABELS = {
    "fluency": "Speaks fluently with a natural, well-paced delivery",
    "confidence": "Comes across as confident and composed",
    "grammar": "Uses grammatically clean, well-structured sentences",
    "vocabulary": "Demonstrates a rich and varied vocabulary",
    "technical": "Shows strong technical/domain knowledge",
    "communication": "Communicates ideas clearly and coherently",
}

STRENGTH_THRESHOLD = 75


def detect_strengths(scores: dict, top_n: int = 3) -> list:
    """
    Args:
        scores: dict of dimension -> score (0-100)

    Returns:
        List of strength descriptions for dimensions scoring above threshold,
        sorted by score descending, capped at top_n.
    """
    strong_dims = [(dim, score) for dim, score in scores.items() if score >= STRENGTH_THRESHOLD]
    strong_dims.sort(key=lambda x: x[1], reverse=True)

    return [
        {"dimension": dim, "score": score, "description": _STRENGTH_LABELS.get(dim, dim.title())}
        for dim, score in strong_dims[:top_n]
    ]

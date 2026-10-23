"""
weakness_detector.py
======================
Identifies a candidate's weakest scoring dimensions so feedback can focus
constructively on the highest-impact areas for improvement.
"""

_WEAKNESS_LABELS = {
    "fluency": "Speech fluency could be improved (pacing / pauses)",
    "confidence": "Could project more confidence and composure",
    "grammar": "Grammar and sentence construction need attention",
    "vocabulary": "Could expand vocabulary and word variety",
    "technical": "Technical depth in answers could be stronger",
    "communication": "Overall communication clarity could improve",
}

WEAKNESS_THRESHOLD = 60


def detect_weaknesses(scores: dict, top_n: int = 3) -> list:
    """
    Args:
        scores: dict of dimension -> score (0-100)

    Returns:
        List of weakness descriptions for dimensions scoring below threshold,
        sorted by score ascending (weakest first), capped at top_n.
    """
    weak_dims = [(dim, score) for dim, score in scores.items() if score < WEAKNESS_THRESHOLD]
    weak_dims.sort(key=lambda x: x[1])

    return [
        {"dimension": dim, "score": score, "description": _WEAKNESS_LABELS.get(dim, dim.title())}
        for dim, score in weak_dims[:top_n]
    ]

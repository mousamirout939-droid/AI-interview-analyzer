"""
improvement_tips.py
=====================
Generates concrete, actionable improvement tips tied to each weak
dimension detected by weakness_detector.py.
"""

_TIPS_BY_DIMENSION = {
    "fluency": [
        "Practice answering common interview questions out loud to build a natural pace.",
        "Record yourself and count filler words ('um', 'like') to build awareness.",
        "Pause briefly to think instead of filling silence with filler words.",
    ],
    "confidence": [
        "Prepare a few strong 'wins' in advance so you can speak about them assertively.",
        "Use affirmative language ('I did', 'I achieved') instead of hedging ('I guess', 'maybe').",
        "Practice power-posing or breathing exercises before interviews to reduce nerves.",
    ],
    "grammar": [
        "Review your answers for subject-verb agreement and sentence completeness.",
        "Practice speaking in complete sentences rather than sentence fragments.",
        "Read your practice answers aloud to catch awkward phrasing.",
    ],
    "vocabulary": [
        "Study role-specific terminology so you can vary your word choice naturally.",
        "Avoid repeating the same adjectives; build a small list of alternatives beforehand.",
        "Summarize technical articles in your own words to expand active vocabulary.",
    ],
    "technical": [
        "Review core concepts relevant to the role before the interview.",
        "Practice explaining technical concepts in simple, structured terms (what/why/how).",
        "Use the STAR method with specific technical details in the 'action' step.",
    ],
    "communication": [
        "Structure answers with a clear beginning, middle, and end (e.g. STAR method).",
        "Keep sentences to a moderate length; avoid overly long run-on answers.",
        "Summarize your key point at the end of each answer for clarity.",
    ],
}


def generate_tips(weaknesses: list) -> list:
    """
    Args:
        weaknesses: output of weakness_detector.detect_weaknesses

    Returns:
        List of {"dimension": ..., "tips": [...]} dicts.
    """
    tips = []
    for weakness in weaknesses:
        dim = weakness["dimension"]
        tips.append({
            "dimension": dim,
            "tips": _TIPS_BY_DIMENSION.get(dim, ["Keep practicing this area with mock interviews."]),
        })
    return tips

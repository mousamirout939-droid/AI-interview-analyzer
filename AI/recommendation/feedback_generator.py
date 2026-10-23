"""
feedback_generator.py
=======================
Generates a human-readable narrative feedback paragraph summarizing a
candidate's performance, combining strengths, weaknesses, and overall
verdict into natural language for the report.
"""

def generate_feedback(overall: dict, strengths: list, weaknesses: list) -> str:
    """
    Args:
        overall: output of AI.scoring.overall_score.calculate_overall_score
        strengths: output of strengths_detector.detect_strengths
        weaknesses: output of weakness_detector.detect_weaknesses

    Returns:
        A short narrative feedback string.
    """
    score = overall.get("overall_score", 0)
    verdict = overall.get("verdict", "Satisfactory")

    parts = [f"Overall, this interview performance is rated '{verdict}' with a score of {score}/100."]

    if strengths:
        strength_text = "; ".join(s["description"] for s in strengths)
        parts.append(f"Key strengths: {strength_text}.")
    else:
        parts.append("No standout strengths were identified above the strong-performance threshold.")

    if weaknesses:
        weakness_text = "; ".join(w["description"] for w in weaknesses)
        parts.append(f"Areas to improve: {weakness_text}.")
    else:
        parts.append("No major weaknesses were detected — performance is consistent across all dimensions.")

    return " ".join(parts)

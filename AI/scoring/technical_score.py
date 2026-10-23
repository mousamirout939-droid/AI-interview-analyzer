"""
technical_score.py
=====================
Scores technical depth (0-100) based on how many domain-relevant
technical keywords (from datasets/technical_keywords.csv) appear in the
candidate's answer, weighted by each keyword's importance weight.
"""

from AI.nlp.keyword_extractor import extract_technical_keywords


def calculate_technical_score(text: str, expected_keyword_count: int = 4) -> dict:
    """
    Args:
        text: transcript text
        expected_keyword_count: rough number of technical terms expected
                                 in a strong answer, used to normalize the score

    Returns:
        {"score": float 0-100, "breakdown": {...}}
    """
    found = extract_technical_keywords(text)
    weighted_sum = sum(k["weight"] for k in found)
    normalized = min(1.0, weighted_sum / max(1, expected_keyword_count))
    score = normalized * 100

    return {
        "score": round(score, 1),
        "breakdown": {
            "technical_terms_found": [k["keyword"] for k in found],
            "term_count": len(found),
            "weighted_sum": round(weighted_sum, 2),
        },
    }

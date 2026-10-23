"""
grammar_score.py
==================
Converts grammar-checker output into a 0-100 score: fewer issues per
sentence yields a higher score.
"""

def calculate_grammar_score(grammar_report: dict) -> dict:
    """
    Args:
        grammar_report: output of AI.nlp.grammer_checker.check_grammar

    Returns:
        {"score": float 0-100, "breakdown": {...}}
    """
    error_rate = grammar_report.get("error_rate", 0.0)
    # error_rate is issues-per-sentence; 0 issues -> 100, 2+ issues/sentence -> near 0
    score = max(0.0, 100 - (error_rate * 45))

    return {
        "score": round(min(100.0, score), 1),
        "breakdown": {
            "issue_count": grammar_report.get("issue_count", 0),
            "sentence_count": grammar_report.get("sentence_count", 0),
            "error_rate": error_rate,
        },
    }

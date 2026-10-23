"""
communication_score.py
========================
Scores overall communication clarity (0-100) combining sentence structure
metrics with grammar quality. Rewards well-formed, moderately complex,
grammatically clean answers.
"""

from AI.nlp.sentence_analyzer import analyze_sentences


def calculate_communication_score(text: str, grammar_score: float) -> dict:
    sentence_stats = analyze_sentences(text)
    avg_len = sentence_stats["avg_sentence_length"]

    # Ideal average sentence length for spoken interview answers: 12-22 words
    if 12 <= avg_len <= 22:
        structure_score = 100
    elif avg_len == 0:
        structure_score = 0
    else:
        distance = min(abs(avg_len - 12), abs(avg_len - 22))
        structure_score = max(0, 100 - distance * 3)

    score = (structure_score * 0.5) + (grammar_score * 0.5)

    return {
        "score": round(min(100.0, score), 1),
        "breakdown": {
            "avg_sentence_length": avg_len,
            "sentence_count": sentence_stats["sentence_count"],
            "structure_score": round(structure_score, 1),
            "grammar_score": grammar_score,
        },
    }

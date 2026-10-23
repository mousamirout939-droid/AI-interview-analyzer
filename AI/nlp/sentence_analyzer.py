"""
sentence_analyzer.py
======================
Analyzes sentence-level structure of a transcript: average sentence
length, sentence length variance, and a naive complexity estimate. These
metrics feed the fluency and communication scorers.
"""

from AI.nlp.tokenizer import tokenize_sentences, tokenize_words


def analyze_sentences(text: str) -> dict:
    sentences = tokenize_sentences(text)
    if not sentences:
        return {
            "sentence_count": 0,
            "avg_sentence_length": 0.0,
            "longest_sentence_words": 0,
            "shortest_sentence_words": 0,
        }

    lengths = [len(tokenize_words(s)) for s in sentences]
    return {
        "sentence_count": len(sentences),
        "avg_sentence_length": round(sum(lengths) / len(lengths), 2),
        "longest_sentence_words": max(lengths),
        "shortest_sentence_words": min(lengths),
    }


def estimate_complexity(text: str) -> str:
    """
    Very lightweight readability heuristic based on average sentence length.
    Returns one of: "simple", "moderate", "complex".
    """
    stats = analyze_sentences(text)
    avg_len = stats["avg_sentence_length"]
    if avg_len == 0:
        return "simple"
    if avg_len < 10:
        return "simple"
    if avg_len < 20:
        return "moderate"
    return "complex"

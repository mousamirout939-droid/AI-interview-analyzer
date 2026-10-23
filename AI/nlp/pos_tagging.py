"""
pos_tagging.py
================
Part-of-speech tagging using NLTK's averaged perceptron tagger, with a
graceful fallback (tags everything as unknown "X") if the tagger data
isn't available so the pipeline never hard-crashes.
"""

from AI.nlp.tokenizer import tokenize_words


def pos_tag_text(text: str) -> list:
    """Return a list of (word, tag) tuples for the given text."""
    tokens = tokenize_words(text)
    if not tokens:
        return []
    try:
        import nltk
        return nltk.pos_tag(tokens)
    except Exception:
        return [(t, "X") for t in tokens]


def count_pos_categories(text: str) -> dict:
    """
    Aggregate POS tags into broad categories (nouns, verbs, adjectives,
    adverbs) - useful signal for vocabulary/communication scoring.
    """
    tags = pos_tag_text(text)
    categories = {"nouns": 0, "verbs": 0, "adjectives": 0, "adverbs": 0, "other": 0}

    for _, tag in tags:
        if tag.startswith("NN"):
            categories["nouns"] += 1
        elif tag.startswith("VB"):
            categories["verbs"] += 1
        elif tag.startswith("JJ"):
            categories["adjectives"] += 1
        elif tag.startswith("RB"):
            categories["adverbs"] += 1
        else:
            categories["other"] += 1

    return categories

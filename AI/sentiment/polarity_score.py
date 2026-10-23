"""
polarity_score.py
====================
Computes sentiment polarity (-1.0 negative to +1.0 positive) for a
transcript using TextBlob, cross-checked against the project's curated
positive/negative word lists for interpretability.
"""

import os
import functools
from textblob import TextBlob

_POS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "datasets", "positive_words.txt")
_NEG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "datasets", "negative_words.txt")


@functools.lru_cache(maxsize=1)
def _load_word_list(path: str) -> set:
    path = os.path.abspath(path)
    if not os.path.exists(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}


def compute_polarity(text: str) -> dict:
    """
    Returns:
        {
            "polarity": float [-1.0, 1.0],
            "label": "positive" | "neutral" | "negative",
            "positive_word_hits": [...],
            "negative_word_hits": [...]
        }
    """
    if not text or not text.strip():
        return {"polarity": 0.0, "label": "neutral", "positive_word_hits": [], "negative_word_hits": []}

    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 3)

    words = [w.strip(".,!?;:").lower() for w in text.split()]
    pos_hits = [w for w in words if w in _load_word_list(_POS_PATH)]
    neg_hits = [w for w in words if w in _load_word_list(_NEG_PATH)]

    # Blend TextBlob's polarity with signal from the curated positive/negative
    # word lists so short, plainly-worded interview answers (which TextBlob's
    # general-purpose model can under-score) are classified more reliably.
    lexicon_signal = (len(pos_hits) - len(neg_hits)) / max(1, len(words))
    blended = polarity + (lexicon_signal * 1.5)

    if blended > 0.1:
        label = "positive"
    elif blended < -0.1:
        label = "negative"
    else:
        label = "neutral"

    return {
        "polarity": polarity,
        "label": label,
        "positive_word_hits": pos_hits,
        "negative_word_hits": neg_hits,
    }

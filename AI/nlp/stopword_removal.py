"""
stopword_removal.py
=====================
Removes common stopwords from tokenized text using the project's
datasets/stopwords.txt list (falls back to NLTK's list if available).
"""

import os
import functools

_DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "datasets", "stopwords.txt")


@functools.lru_cache(maxsize=1)
def _load_stopwords() -> set:
    path = os.path.abspath(_DATASET_PATH)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return {line.strip().lower() for line in f if line.strip()}
    try:
        from nltk.corpus import stopwords
        return set(stopwords.words("english"))
    except Exception:
        return set()


def remove_stopwords(tokens: list) -> list:
    """Filter a list of word tokens, removing stopwords (case-insensitive)."""
    stopwords_set = _load_stopwords()
    return [t for t in tokens if t.lower() not in stopwords_set]


def get_stopwords() -> set:
    return _load_stopwords()

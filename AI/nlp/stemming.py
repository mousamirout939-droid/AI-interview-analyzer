"""
stemming.py
============
Reduces words to their root/stem form using NLTK's Porter Stemmer, with a
minimal rule-based fallback if NLTK isn't available.
"""

_SUFFIXES = ["ing", "edly", "edness", "ed", "ies", "es", "s", "ly"]


def _basic_stem(word: str) -> str:
    lower = word.lower()
    for suf in sorted(_SUFFIXES, key=len, reverse=True):
        if lower.endswith(suf) and len(lower) - len(suf) >= 3:
            return lower[: -len(suf)]
    return lower


def stem_word(word: str) -> str:
    try:
        from nltk.stem import PorterStemmer
        return PorterStemmer().stem(word)
    except Exception:
        return _basic_stem(word)


def stem_tokens(tokens: list) -> list:
    try:
        from nltk.stem import PorterStemmer
        stemmer = PorterStemmer()
        return [stemmer.stem(t) for t in tokens]
    except Exception:
        return [_basic_stem(t) for t in tokens]

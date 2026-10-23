"""
tokenizer.py
=============
Sentence and word tokenization utilities built on NLTK, with a
dependency-free regex fallback so the pipeline still functions if the
NLTK punkt data hasn't been downloaded yet (e.g. constrained environments).
"""

import re
import logging

logger = logging.getLogger("ai_interview_analyzer.tokenizer")

_WORD_RE = re.compile(r"[A-Za-z']+")
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def _nltk_available() -> bool:
    try:
        import nltk  # noqa: F401
        from nltk.tokenize import word_tokenize, sent_tokenize  # noqa: F401
        word_tokenize("test sentence.")
        return True
    except Exception:
        return False


def tokenize_words(text: str) -> list:
    """Return a list of word tokens (alphabetic only, punctuation stripped)."""
    if not text:
        return []
    if _nltk_available():
        from nltk.tokenize import word_tokenize
        return [t for t in word_tokenize(text) if re.match(r"^[A-Za-z']+$", t)]
    return _WORD_RE.findall(text)


def tokenize_sentences(text: str) -> list:
    """Return a list of sentences."""
    if not text:
        return []
    if _nltk_available():
        from nltk.tokenize import sent_tokenize
        return [s.strip() for s in sent_tokenize(text) if s.strip()]
    return [s.strip() for s in _SENTENCE_SPLIT_RE.split(text) if s.strip()]


def word_count(text: str) -> int:
    return len(tokenize_words(text))


def sentence_count(text: str) -> int:
    return len(tokenize_sentences(text))

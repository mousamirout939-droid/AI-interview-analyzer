"""
text_cleaner.py
=================
Normalizes raw transcript text before further NLP processing: lowercasing,
whitespace collapsing, punctuation normalization, and removal of
transcription artifacts.
"""

import re

_MULTI_SPACE_RE = re.compile(r"\s+")
_PUNCT_SPACING_RE = re.compile(r"\s+([.,!?;:])")
_NON_PRINTABLE_RE = re.compile(r"[^\x20-\x7E]+")


def clean_text(text: str, lowercase: bool = False) -> str:
    """Collapse whitespace, strip stray punctuation spacing and non-printable chars."""
    if not text:
        return ""

    text = _NON_PRINTABLE_RE.sub(" ", text)
    text = _PUNCT_SPACING_RE.sub(r"\1", text)
    text = _MULTI_SPACE_RE.sub(" ", text).strip()

    if lowercase:
        text = text.lower()

    return text


def remove_repeated_words(text: str) -> str:
    """Remove immediate word repetitions common in spoken transcripts (e.g. 'the the')."""
    words = text.split()
    cleaned = []
    for i, word in enumerate(words):
        if i > 0 and word.lower() == words[i - 1].lower():
            continue
        cleaned.append(word)
    return " ".join(cleaned)


def normalize_transcript(raw_text: str) -> str:
    """Full normalization pipeline applied to a raw transcript before NLP analysis."""
    text = clean_text(raw_text)
    text = remove_repeated_words(text)
    return text

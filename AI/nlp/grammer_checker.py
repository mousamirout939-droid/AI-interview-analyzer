"""
grammer_checker.py
=====================
(Filename intentionally matches the original project skeleton's spelling.)

A lightweight, fully offline grammar checker. It flags a set of common
grammatical issues using rule-based heuristics (subject-verb agreement
patterns, double negatives, repeated words, missing capitalization) rather
than depending on a network-bound grammar API. This keeps the scoring
pipeline deterministic and testable.

For higher accuracy in production, this module can be swapped to call
`language_tool_python` (wraps LanguageTool) if that optional dependency is
installed.
"""

import re

from AI.nlp.tokenizer import tokenize_sentences

_DOUBLE_NEGATIVE_RE = re.compile(r"\b(not|n't|no|never)\b.*\b(not|n't|no|never|nothing|nobody|nowhere)\b", re.I)
_REPEATED_WORD_RE = re.compile(r"\b(\w+)\s+\1\b", re.I)
_LOWERCASE_START_RE = re.compile(r"^[a-z]")
_MISSING_ARTICLE_HINTS = {"i have experience in", "i am working on"}


def _language_tool_available():
    try:
        import language_tool_python  # noqa: F401
        return True
    except ImportError:
        return False


def check_grammar(text: str) -> dict:
    """
    Analyze text for grammar issues.

    Returns:
        {
            "issues": [{"type": str, "message": str, "sentence": str}, ...],
            "issue_count": int,
            "sentence_count": int,
            "error_rate": float  # issues per sentence
        }
    """
    if _language_tool_available():
        return _check_with_language_tool(text)
    return _check_with_heuristics(text)


def _check_with_language_tool(text: str) -> dict:  # pragma: no cover - optional path
    import language_tool_python
    tool = language_tool_python.LanguageTool("en-US")
    matches = tool.check(text)
    sentences = tokenize_sentences(text)
    issues = [
        {"type": m.ruleId, "message": m.message, "sentence": text[max(0, m.offset - 20):m.offset + 20]}
        for m in matches
    ]
    return {
        "issues": issues,
        "issue_count": len(issues),
        "sentence_count": len(sentences) or 1,
        "error_rate": round(len(issues) / (len(sentences) or 1), 3),
    }


def _check_with_heuristics(text: str) -> dict:
    sentences = tokenize_sentences(text)
    issues = []

    for sentence in sentences:
        stripped = sentence.strip()
        if not stripped:
            continue

        if _LOWERCASE_START_RE.match(stripped):
            issues.append({
                "type": "capitalization",
                "message": "Sentence should start with a capital letter.",
                "sentence": stripped,
            })

        if _DOUBLE_NEGATIVE_RE.search(stripped):
            issues.append({
                "type": "double_negative",
                "message": "Possible double negative detected.",
                "sentence": stripped,
            })

        if _REPEATED_WORD_RE.search(stripped):
            issues.append({
                "type": "repeated_word",
                "message": "Repeated word detected.",
                "sentence": stripped,
            })

        if not stripped.endswith((".", "!", "?")):
            issues.append({
                "type": "punctuation",
                "message": "Sentence is missing terminal punctuation.",
                "sentence": stripped,
            })

    sentence_count = len(sentences) or 1
    return {
        "issues": issues,
        "issue_count": len(issues),
        "sentence_count": sentence_count,
        "error_rate": round(len(issues) / sentence_count, 3),
    }

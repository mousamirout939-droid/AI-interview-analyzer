"""
keyword_extractor.py
======================
Extracts salient keywords from a transcript using a TF-based frequency
ranking (with stopword removal), and separately flags which recognized
technical/domain keywords (from datasets/technical_keywords.csv) appear in
the answer. This dual output feeds both the vocabulary scorer and the
technical scorer.
"""

import os
import csv
import functools
from collections import Counter

from AI.nlp.tokenizer import tokenize_words
from AI.nlp.stopword_removal import remove_stopwords

_TECH_KEYWORDS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "datasets", "technical_keywords.csv")


@functools.lru_cache(maxsize=1)
def _load_technical_keywords() -> list:
    path = os.path.abspath(_TECH_KEYWORDS_PATH)
    keywords = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                keywords.append({
                    "keyword": row["keyword"].strip().lower(),
                    "domain": row.get("domain", "general"),
                    "weight": float(row.get("weight", 1.0)),
                })
    return keywords


def extract_top_keywords(text: str, top_n: int = 10) -> list:
    """Return the top-N most frequent non-stopword tokens with counts."""
    tokens = remove_stopwords([t.lower() for t in tokenize_words(text)])
    tokens = [t for t in tokens if len(t) > 2]
    counts = Counter(tokens)
    return [{"keyword": word, "count": count} for word, count in counts.most_common(top_n)]


def extract_technical_keywords(text: str) -> list:
    """Return the technical/domain keywords (multi-word aware) found in the text."""
    import re
    lower_text = text.lower()
    found = []
    for entry in _load_technical_keywords():
        pattern = r"(?<![a-z0-9])" + re.escape(entry["keyword"]) + r"(?![a-z0-9])"
        if re.search(pattern, lower_text):
            found.append(entry)
    return found


def keyword_density(text: str) -> float:
    """Fraction of total words that are non-stopword 'content' words."""
    all_tokens = tokenize_words(text)
    if not all_tokens:
        return 0.0
    content_tokens = remove_stopwords([t.lower() for t in all_tokens])
    return round(len(content_tokens) / len(all_tokens), 3)

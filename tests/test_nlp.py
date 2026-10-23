"""
test_nlp.py
=============
Unit tests for the NLP layer: tokenization, stopword removal, keyword
extraction, and filler word detection.
"""

from AI.nlp.tokenizer import tokenize_words, tokenize_sentences
from AI.nlp.stopword_removal import remove_stopwords
from AI.nlp.keyword_extractor import extract_top_keywords, extract_technical_keywords
from AI.nlp.filler_word_detector import detect_filler_words
from AI.nlp.text_cleaner import normalize_transcript


def test_tokenize_words():
    words = tokenize_words("I really enjoy solving hard problems.")
    assert "enjoy" in [w.lower() for w in words]
    assert len(words) >= 5


def test_tokenize_sentences():
    sentences = tokenize_sentences("This is one sentence. This is another one!")
    assert len(sentences) == 2


def test_remove_stopwords():
    filtered = remove_stopwords(["the", "quick", "brown", "fox", "is", "running"])
    assert "the" not in filtered
    assert "quick" in filtered


def test_extract_top_keywords():
    keywords = extract_top_keywords("Python python python is great for data science and machine learning")
    assert keywords[0]["keyword"] == "python"


def test_extract_technical_keywords():
    found = extract_technical_keywords("I designed a scalable microservices architecture using docker.")
    keywords_found = [k["keyword"] for k in found]
    assert "microservices" in keywords_found
    assert "docker" in keywords_found


def test_detect_filler_words():
    result = detect_filler_words("Um, so, I, uh, worked on this project, you know, for a while.")
    assert result["total_fillers"] >= 3


def test_normalize_transcript_collapses_repeats():
    normalized = normalize_transcript("I I really really like like coding")
    assert "I really like coding" in normalized

"""
nlp_pipeline.py
=================
Stage 3 pipeline: runs the full NLP + sentiment analysis suite over a
cleaned transcript.
"""

import logging

from AI.nlp.tokenizer import tokenize_words, tokenize_sentences
from AI.nlp.stopword_removal import remove_stopwords
from AI.nlp.keyword_extractor import extract_top_keywords, extract_technical_keywords
from AI.nlp.sentence_analyzer import analyze_sentences, estimate_complexity
from AI.nlp.grammer_checker import check_grammar
from AI.nlp.filler_word_detector import detect_filler_words
from AI.sentiment.sentiment_analysis import analyze_sentiment

logger = logging.getLogger("ai_interview_analyzer.nlp_pipeline")


def run_nlp_analysis(cleaned_text: str) -> dict:
    """
    Returns a consolidated dict of all NLP + sentiment signals used as
    input to the scoring pipeline.
    """
    words = tokenize_words(cleaned_text)
    sentences = tokenize_sentences(cleaned_text)
    content_words = remove_stopwords([w.lower() for w in words])

    transcript_stats = {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "content_word_count": len(content_words),
    }

    result = {
        "transcript_stats": transcript_stats,
        "top_keywords": extract_top_keywords(cleaned_text),
        "technical_keywords": extract_technical_keywords(cleaned_text),
        "sentence_analysis": analyze_sentences(cleaned_text),
        "complexity": estimate_complexity(cleaned_text),
        "grammar": check_grammar(cleaned_text),
        "filler_words": detect_filler_words(cleaned_text),
        "sentiment": analyze_sentiment(cleaned_text),
    }

    logger.info("NLP pipeline complete: %s words, %s sentences", len(words), len(sentences))
    return result

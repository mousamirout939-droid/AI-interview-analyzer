"""
scoring_pipeline.py
=====================
Stage 4 pipeline: converts NLP/sentiment/audio signals into the six
dimension scores plus the weighted overall score.
"""

import logging

from AI.scoring.fluency_score import calculate_fluency_score
from AI.scoring.confidence_score import calculate_confidence_score
from AI.scoring.grammar_score import calculate_grammar_score
from AI.scoring.vocabulary_score import calculate_vocabulary_score
from AI.scoring.technical_score import calculate_technical_score
from AI.scoring.communication_score import calculate_communication_score
from AI.scoring.overall_score import calculate_overall_score

logger = logging.getLogger("ai_interview_analyzer.scoring_pipeline")


def run_scoring(cleaned_text: str, nlp_result: dict, pause_stats: dict, duration_seconds: float) -> dict:
    """
    Args:
        cleaned_text: normalized transcript text.
        nlp_result: output of nlp_pipeline.run_nlp_analysis.
        pause_stats: output of AI.speech.silence_detection.compute_pause_statistics.
        duration_seconds: total audio duration.

    Returns:
        {
            "fluency": {...}, "confidence": {...}, "grammar": {...},
            "vocabulary": {...}, "technical": {...}, "communication": {...},
            "overall": {...}
        }
    """
    word_count = nlp_result["transcript_stats"]["word_count"]

    fluency = calculate_fluency_score(nlp_result["filler_words"], pause_stats, word_count, duration_seconds)
    confidence = calculate_confidence_score(nlp_result["sentiment"]["emotion"], nlp_result["filler_words"])
    grammar = calculate_grammar_score(nlp_result["grammar"])
    vocabulary = calculate_vocabulary_score(cleaned_text)
    technical = calculate_technical_score(cleaned_text)
    communication = calculate_communication_score(cleaned_text, grammar["score"])

    dimension_scores = {
        "fluency": fluency["score"],
        "confidence": confidence["score"],
        "grammar": grammar["score"],
        "vocabulary": vocabulary["score"],
        "technical": technical["score"],
        "communication": communication["score"],
    }
    overall = calculate_overall_score(dimension_scores)

    logger.info("Scoring pipeline complete: overall=%s", overall["overall_score"])

    return {
        "fluency": fluency,
        "confidence": confidence,
        "grammar": grammar,
        "vocabulary": vocabulary,
        "technical": technical,
        "communication": communication,
        "overall": overall,
    }

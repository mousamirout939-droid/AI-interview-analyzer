"""
report_pipeline.py
=====================
Stage 5 pipeline: turns scoring output into strengths/weaknesses/tips and
a final structured interview summary object (ready for persistence and
PDF/HTML rendering).
"""

import logging

from AI.recommendation.strengths_detector import detect_strengths
from AI.recommendation.weakness_detector import detect_weaknesses
from AI.recommendation.improvement_tips import generate_tips
from AI.recommendation.feedback_generator import generate_feedback
from AI.recommendation.interview_summary import build_interview_summary

logger = logging.getLogger("ai_interview_analyzer.report_pipeline")


def run_report_generation(nlp_result: dict, scoring_result: dict) -> dict:
    dimension_scores = {
        "fluency": scoring_result["fluency"]["score"],
        "confidence": scoring_result["confidence"]["score"],
        "grammar": scoring_result["grammar"]["score"],
        "vocabulary": scoring_result["vocabulary"]["score"],
        "technical": scoring_result["technical"]["score"],
        "communication": scoring_result["communication"]["score"],
    }

    strengths = detect_strengths(dimension_scores)
    weaknesses = detect_weaknesses(dimension_scores)
    tips = generate_tips(weaknesses)
    feedback = generate_feedback(scoring_result["overall"], strengths, weaknesses)

    summary = build_interview_summary(
        transcript_stats=nlp_result["transcript_stats"],
        sentiment=nlp_result["sentiment"],
        scores=dimension_scores,
        overall=scoring_result["overall"],
        strengths=strengths,
        weaknesses=weaknesses,
        tips=tips,
        feedback=feedback,
    )

    logger.info("Report pipeline complete.")
    return summary

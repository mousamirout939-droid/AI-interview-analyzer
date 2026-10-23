"""
evaluator.py
==============
Runs the AI pipeline against a labeled sample dataset (datasets/sample_transcripts.csv)
to sanity-check that scoring functions behave consistently and stay within
expected numeric bounds. Intended for use in CI or manual model validation,
not as part of the live request path.
"""

import csv
import logging
import os

from AI.pipeline.nlp_pipeline import run_nlp_analysis
from AI.pipeline.scoring_pipeline import run_scoring
from evaluation.metrics import score_distribution_stats

logger = logging.getLogger("ai_interview_analyzer.evaluator")

_SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "..", "datasets", "sample_transcripts.csv")


def evaluate_sample_transcripts() -> dict:
    """
    Run the NLP + scoring pipeline (text-only, no audio) over the bundled
    sample transcripts and return aggregate score statistics per dimension.
    """
    path = os.path.abspath(_SAMPLE_PATH)
    if not os.path.exists(path):
        logger.warning("Sample transcript dataset not found at %s", path)
        return {}

    dimension_scores = {
        "fluency": [], "confidence": [], "grammar": [],
        "vocabulary": [], "technical": [], "communication": [], "overall": [],
    }

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row["transcript"]
            nlp_result = run_nlp_analysis(text)
            # No real audio available for text-only evaluation; assume a
            # neutral pause profile and reasonable spoken duration estimate.
            pause_stats = {"speaking_ratio": 0.85, "avg_pause_ms": 400, "num_pauses": 2, "total_pause_ms": 800, "total_duration_ms": 20000}
            word_count = nlp_result["transcript_stats"]["word_count"]
            estimated_duration = max(5.0, word_count / 2.2)  # ~130 wpm estimate

            scoring_result = run_scoring(text, nlp_result, pause_stats, estimated_duration)

            for dim in ["fluency", "confidence", "grammar", "vocabulary", "technical", "communication"]:
                dimension_scores[dim].append(scoring_result[dim]["score"])
            dimension_scores["overall"].append(scoring_result["overall"]["overall_score"])

    return {dim: score_distribution_stats(scores) for dim, scores in dimension_scores.items()}

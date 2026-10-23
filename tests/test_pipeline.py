"""
test_pipeline.py
===================
Integration-style test for the text-based portion of the pipeline
(NLP -> scoring -> report), bypassing audio processing since CI
environments may not have real interview audio available.
"""

from AI.pipeline.nlp_pipeline import run_nlp_analysis
from AI.pipeline.scoring_pipeline import run_scoring
from AI.pipeline.report_pipeline import run_report_generation


SAMPLE_TRANSCRIPT = (
    "I have three years of experience building scalable backend systems using Python "
    "and microservices architecture. I successfully led a project that improved "
    "database query performance significantly. I am confident in my problem solving "
    "and communication skills."
)


def test_nlp_to_scoring_to_report_pipeline():
    nlp_result = run_nlp_analysis(SAMPLE_TRANSCRIPT)
    assert nlp_result["transcript_stats"]["word_count"] > 0

    pause_stats = {"speaking_ratio": 0.88, "avg_pause_ms": 250, "num_pauses": 3,
                    "total_pause_ms": 750, "total_duration_ms": 30000}
    scoring_result = run_scoring(SAMPLE_TRANSCRIPT, nlp_result, pause_stats, duration_seconds=30.0)

    for dim in ["fluency", "confidence", "grammar", "vocabulary", "technical", "communication"]:
        assert 0 <= scoring_result[dim]["score"] <= 100

    assert 0 <= scoring_result["overall"]["overall_score"] <= 100

    summary = run_report_generation(nlp_result, scoring_result)
    assert "feedback" in summary
    assert "dimension_scores" in summary
    assert isinstance(summary["strengths"], list)
    assert isinstance(summary["weaknesses"], list)

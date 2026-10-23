"""
test_scoring.py
==================
Unit tests for the scoring layer: individual dimension scorers and the
overall weighted score / candidate ranker.
"""

from AI.scoring.fluency_score import calculate_fluency_score
from AI.scoring.confidence_score import calculate_confidence_score
from AI.scoring.grammar_score import calculate_grammar_score
from AI.scoring.vocabulary_score import calculate_vocabulary_score
from AI.scoring.technical_score import calculate_technical_score
from AI.scoring.overall_score import calculate_overall_score
from AI.scoring.candidate_ranker import rank_candidates


def test_fluency_score_in_range():
    filler_stats = {"filler_rate_per_100_words": 2.0}
    pause_stats = {"speaking_ratio": 0.9, "avg_pause_ms": 300}
    result = calculate_fluency_score(filler_stats, pause_stats, word_count=150, duration_seconds=75)
    assert 0 <= result["score"] <= 100


def test_confidence_score_in_range():
    emotion = {"confidence": 0.8, "nervousness": 0.2, "calmness": 0.7}
    filler_stats = {"filler_rate_per_100_words": 1.5}
    result = calculate_confidence_score(emotion, filler_stats)
    assert 0 <= result["score"] <= 100


def test_grammar_score_perfect():
    grammar_report = {"issue_count": 0, "sentence_count": 5, "error_rate": 0.0}
    result = calculate_grammar_score(grammar_report)
    assert result["score"] == 100.0


def test_vocabulary_score_empty_text():
    result = calculate_vocabulary_score("")
    assert result["score"] == 0.0


def test_technical_score_detects_terms():
    result = calculate_technical_score("I used docker and kubernetes to manage microservices architecture.")
    assert result["score"] > 0
    assert "docker" in result["breakdown"]["technical_terms_found"]


def test_overall_score_weighted_average():
    scores = {"fluency": 80, "confidence": 80, "grammar": 80, "vocabulary": 80, "technical": 80, "communication": 80}
    result = calculate_overall_score(scores)
    assert result["overall_score"] == 80.0
    assert result["verdict"] == "Strong"


def test_candidate_ranker_assigns_ranks():
    candidates = [
        {"id": 1, "name": "A", "overall_score": 60},
        {"id": 2, "name": "B", "overall_score": 90},
        {"id": 3, "name": "C", "overall_score": 75},
    ]
    ranked = rank_candidates(candidates)
    assert ranked[0]["name"] == "B"
    assert ranked[0]["rank"] == 1
    assert ranked[-1]["name"] == "A"

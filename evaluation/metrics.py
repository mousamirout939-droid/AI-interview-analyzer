"""
metrics.py
============
General-purpose evaluation metrics for validating scoring consistency and
model output quality (used by evaluator.py and the test suite).
"""

import statistics


def mean_absolute_error(predicted: list, actual: list) -> float:
    if not predicted or len(predicted) != len(actual):
        return 0.0
    errors = [abs(p - a) for p, a in zip(predicted, actual)]
    return round(sum(errors) / len(errors), 3)


def root_mean_squared_error(predicted: list, actual: list) -> float:
    if not predicted or len(predicted) != len(actual):
        return 0.0
    squared_errors = [(p - a) ** 2 for p, a in zip(predicted, actual)]
    return round((sum(squared_errors) / len(squared_errors)) ** 0.5, 3)


def score_distribution_stats(scores: list) -> dict:
    if not scores:
        return {"mean": 0, "median": 0, "stdev": 0, "min": 0, "max": 0}
    return {
        "mean": round(statistics.mean(scores), 2),
        "median": round(statistics.median(scores), 2),
        "stdev": round(statistics.pstdev(scores), 2) if len(scores) > 1 else 0.0,
        "min": round(min(scores), 2),
        "max": round(max(scores), 2),
    }


def consistency_score(scores_run_a: list, scores_run_b: list) -> float:
    """
    Measures how consistent two scoring runs of the same transcripts are
    (1.0 = perfectly consistent, 0.0 = maximally inconsistent), based on
    normalized mean absolute difference.
    """
    if not scores_run_a or len(scores_run_a) != len(scores_run_b):
        return 0.0
    diffs = [abs(a - b) for a, b in zip(scores_run_a, scores_run_b)]
    avg_diff = sum(diffs) / len(diffs)
    return round(max(0.0, 1 - (avg_diff / 100)), 3)

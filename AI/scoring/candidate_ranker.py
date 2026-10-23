"""
candidate_ranker.py
=====================
Ranks a list of candidates/interviews by overall score (descending),
assigning rank positions and percentile standing. Used by the ranking
service/blueprint to populate the leaderboard view.
"""


def rank_candidates(candidates: list) -> list:
    """
    Args:
        candidates: list of dicts, each containing at minimum
                    {"id": ..., "name": ..., "overall_score": float}

    Returns:
        The same list, sorted descending by overall_score, with "rank" and
        "percentile" keys added to each entry.
    """
    sorted_candidates = sorted(candidates, key=lambda c: c.get("overall_score", 0), reverse=True)
    total = len(sorted_candidates) or 1

    for idx, candidate in enumerate(sorted_candidates, start=1):
        candidate["rank"] = idx
        candidate["percentile"] = round((1 - (idx - 1) / total) * 100, 1)

    return sorted_candidates


def top_n_candidates(candidates: list, n: int = 10) -> list:
    return rank_candidates(candidates)[:n]

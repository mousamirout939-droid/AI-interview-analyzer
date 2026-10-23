"""
vocabulary_score.py
=====================
Scores vocabulary richness (0-100) using lexical diversity (unique words /
total words) and content-word density.
"""

from AI.nlp.tokenizer import tokenize_words
from AI.nlp.keyword_extractor import keyword_density


def calculate_vocabulary_score(text: str) -> dict:
    words = [w.lower() for w in tokenize_words(text)]
    if not words:
        return {"score": 0.0, "breakdown": {"lexical_diversity": 0.0, "keyword_density": 0.0, "unique_words": 0, "total_words": 0}}

    unique_words = len(set(words))
    total_words = len(words)
    lexical_diversity = unique_words / total_words

    density = keyword_density(text)

    # Lexical diversity of ~0.5-0.7 is typical for fluent spontaneous speech;
    # scale so 0.6 diversity + high density approaches 100.
    diversity_component = min(1.0, lexical_diversity / 0.65) * 60
    density_component = min(1.0, density / 0.55) * 40

    score = diversity_component + density_component

    return {
        "score": round(min(100.0, score), 1),
        "breakdown": {
            "lexical_diversity": round(lexical_diversity, 3),
            "keyword_density": density,
            "unique_words": unique_words,
            "total_words": total_words,
        },
    }

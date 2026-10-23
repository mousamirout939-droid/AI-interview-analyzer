"""
AI package
===========
Root package for the interview analysis AI/ML pipeline: speech
processing, NLP, sentiment analysis, scoring, and recommendations.

This module also configures NLTK's data search path to include the
project's local models/nltk cache (populated by scripts/download_models.py)
so corpora are found without relying on the system-wide NLTK data
directory.
"""

import os

try:
    import nltk
    _NLTK_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "models", "nltk")
    _NLTK_DATA_DIR = os.path.abspath(_NLTK_DATA_DIR)
    if os.path.isdir(_NLTK_DATA_DIR) and _NLTK_DATA_DIR not in nltk.data.path:
        nltk.data.path.insert(0, _NLTK_DATA_DIR)
except ImportError:
    pass

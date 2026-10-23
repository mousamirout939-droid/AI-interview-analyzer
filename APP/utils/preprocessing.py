"""
preprocessing.py
===================
Application-layer preprocessing helpers that sit between the web
controllers and the AI package: resolving upload folder paths per
interview and building the folder dict expected by
AI.pipeline.complete_pipeline.run_complete_analysis.
"""

from flask import current_app


def build_pipeline_folders() -> dict:
    """Build the folder-path dict expected by the AI complete_pipeline, sourced from app config."""
    cfg = current_app.config
    return {
        "extracted": cfg["AUDIO_EXTRACTED_FOLDER"],
        "cleaned": cfg["AUDIO_CLEANED_FOLDER"],
        "noise_removed": cfg["AUDIO_NOISE_REMOVED_FOLDER"],
        "raw": cfg["TRANSCRIPT_RAW_FOLDER"],
        "cleaned_transcript": cfg["TRANSCRIPT_CLEANED_FOLDER"],
        "json": cfg["TRANSCRIPT_JSON_FOLDER"],
    }

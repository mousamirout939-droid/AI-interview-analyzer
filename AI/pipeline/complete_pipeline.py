"""
complete_pipeline.py
=======================
End-to-end orchestrator: media file in -> full interview analysis summary
out. This is the single entry point the Flask service layer calls after a
video/audio upload.
"""

import os
import logging
from datetime import datetime, timezone

from AI.pipeline.preprocessing_pipeline import run_preprocessing
from AI.pipeline.transcription_pipeline import run_transcription
from AI.pipeline.nlp_pipeline import run_nlp_analysis
from AI.pipeline.scoring_pipeline import run_scoring
from AI.pipeline.report_pipeline import run_report_generation

logger = logging.getLogger("ai_interview_analyzer.complete_pipeline")


def run_complete_analysis(source_path: str, base_filename: str, folders: dict,
                           backend: str = "google", model_size: str = "base",
                           models_dir: str = "models/whisper") -> dict:
    """
    Run the full pipeline: preprocessing -> transcription -> NLP -> scoring -> report.

    Args:
        source_path: path to the uploaded video/audio file.
        base_filename: unique base filename (no extension) used across all
                        pipeline artifacts, e.g. f"interview_{interview_id}".
        folders: dict with keys extracted, cleaned, noise_removed, raw,
                 cleaned_transcript, json for output directories (see
                 config.py for the canonical values).
        backend: transcription backend ("google" or "whisper").
        model_size: whisper model size (ignored for google backend).
        models_dir: local whisper model cache directory.

    Returns:
        A fully structured analysis summary dict, ready to persist.
    """
    started_at = datetime.now(timezone.utc)
    logger.info("Starting complete pipeline for %s", base_filename)

    audio_paths = run_preprocessing(
        source_path=source_path,
        extracted_dir=folders["extracted"],
        cleaned_dir=folders["cleaned"],
        noise_removed_dir=folders["noise_removed"],
        base_filename=base_filename,
    )

    transcription = run_transcription(
        audio_path=audio_paths["noise_removed"],
        raw_dir=folders["raw"],
        cleaned_dir=folders["cleaned_transcript"],
        json_dir=folders["json"],
        base_filename=base_filename,
        backend=backend,
        model_size=model_size,
        models_dir=models_dir,
    )

    nlp_result = run_nlp_analysis(transcription["cleaned_text"])

    scoring_result = run_scoring(
        cleaned_text=transcription["cleaned_text"],
        nlp_result=nlp_result,
        pause_stats=transcription["pause_stats"],
        duration_seconds=transcription["duration_seconds"],
    )

    summary = run_report_generation(nlp_result, scoring_result)
    summary["audio_paths"] = audio_paths
    summary["transcript_paths"] = {
        "raw": transcription["raw_path"],
        "cleaned": transcription["cleaned_path"],
        "json": transcription["json_path"],
    }
    summary["raw_transcript"] = transcription["raw_text"]
    summary["cleaned_transcript"] = transcription["cleaned_text"]
    summary["language"] = transcription["language"]
    summary["duration_seconds"] = transcription["duration_seconds"]

    finished_at = datetime.now(timezone.utc)
    summary["processing_time_seconds"] = round((finished_at - started_at).total_seconds(), 2)

    logger.info(
        "Complete pipeline finished for %s in %.2fs (overall score=%s)",
        base_filename, summary["processing_time_seconds"], summary["overall"]["overall_score"],
    )

    return summary

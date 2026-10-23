"""
interview_service.py
=======================
Creates Interview records and orchestrates the AI pipeline run, persisting
results into Transcript/Analysis/Report rows. This is the main service
called by upload_controller.py and analysis_controller.py.
"""

import json
import logging
from datetime import datetime, timezone

from flask import current_app

from APP.database import db, Interview, Transcript, Analysis, Report
from APP.utils.preprocessing import build_pipeline_folders
from APP.utils.constants import (
    INTERVIEW_STATUS_PROCESSING, INTERVIEW_STATUS_COMPLETED, INTERVIEW_STATUS_FAILED,
)
from AI.pipeline.complete_pipeline import run_complete_analysis

logger = logging.getLogger("ai_interview_analyzer.interview_service")


def create_interview(user_id: int, title: str, question: str, file_type: str,
                      original_filename: str, stored_filename: str, size_bytes: int) -> Interview:
    interview = Interview(
        user_id=user_id,
        title=title or "Untitled Interview",
        question=question,
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_type=file_type,
        file_size_bytes=size_bytes,
        status="uploaded",
    )
    db.session.add(interview)
    db.session.commit()
    return interview


def process_interview(interview_id: int) -> Interview:
    """
    Run the full AI pipeline for the given interview and persist the
    resulting Transcript/Analysis/Report rows. Safe to call synchronously
    for a demo/dev deployment; in a high-throughput production deployment
    this would be dispatched to a background worker (Celery/RQ) instead.
    """
    interview = db.session.get(Interview, interview_id)
    if interview is None:
        raise ValueError(f"Interview {interview_id} not found")

    interview.status = INTERVIEW_STATUS_PROCESSING
    db.session.commit()

    try:
        source_path = interview.stored_path()
        folders = build_pipeline_folders()
        backend = current_app.config.get("TRANSCRIPTION_BACKEND", "google")
        model_size = current_app.config.get("WHISPER_MODEL_SIZE", "base")
        models_dir = current_app.config.get("MODELS_DIR")

        summary = run_complete_analysis(
            source_path=source_path,
            base_filename=f"interview_{interview.id}",
            folders=folders,
            backend=backend,
            model_size=model_size,
            models_dir=models_dir,
        )

        _persist_pipeline_results(interview, summary)

        interview.status = INTERVIEW_STATUS_COMPLETED
        interview.duration_seconds = summary.get("duration_seconds")
        interview.processed_at = datetime.now(timezone.utc)
        db.session.commit()
        logger.info("Interview %s processed successfully.", interview.id)

    except Exception as exc:
        logger.exception("Failed to process interview %s: %s", interview.id, exc)
        interview.status = INTERVIEW_STATUS_FAILED
        interview.error_message = str(exc)
        db.session.commit()
        raise

    return interview


def _persist_pipeline_results(interview: Interview, summary: dict) -> None:
    transcript = Transcript(
        interview_id=interview.id,
        raw_text=summary.get("raw_transcript"),
        cleaned_text=summary.get("cleaned_transcript"),
        language_code=summary.get("language", {}).get("language"),
        language_confidence=summary.get("language", {}).get("confidence"),
        transcription_engine="pipeline",
        raw_path=summary.get("transcript_paths", {}).get("raw"),
        cleaned_path=summary.get("transcript_paths", {}).get("cleaned"),
        json_path=summary.get("transcript_paths", {}).get("json"),
    )
    db.session.add(transcript)

    scores = summary["dimension_scores"]
    overall = summary["overall"]
    sentiment = summary["sentiment"]

    analysis = Analysis(
        interview_id=interview.id,
        fluency_score=scores["fluency"],
        confidence_score=scores["confidence"],
        grammar_score=scores["grammar"],
        vocabulary_score=scores["vocabulary"],
        technical_score=scores["technical"],
        communication_score=scores["communication"],
        overall_score=overall["overall_score"],
        verdict=overall["verdict"],
        sentiment_label=sentiment["polarity"]["label"],
        sentiment_polarity=sentiment["polarity"]["polarity"],
        dominant_emotion=sentiment["emotion"]["dominant_emotion"],
        word_count=summary["transcript_stats"]["word_count"],
        filler_word_count=summary["transcript_stats"].get("content_word_count"),
        raw_summary_json=json.dumps(summary, default=str),
    )
    db.session.add(analysis)

    report = Report(
        interview_id=interview.id,
        feedback_text=summary.get("feedback"),
        strengths_json=json.dumps(summary.get("strengths", [])),
        weaknesses_json=json.dumps(summary.get("weaknesses", [])),
        tips_json=json.dumps(summary.get("improvement_tips", [])),
    )
    db.session.add(report)

    db.session.commit()

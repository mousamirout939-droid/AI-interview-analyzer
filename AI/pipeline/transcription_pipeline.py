"""
transcription_pipeline.py
===========================
Stage 2 pipeline: transcribes preprocessed audio into text and persists
raw/cleaned/json transcript artifacts to disk.
"""

import os
import json
import logging

from AI.speech.speech_to_text import transcribe_audio
from AI.speech.language_detector import detect_language
from AI.speech.silence_detection import compute_pause_statistics
from AI.speech.audio_extractor import get_audio_duration_seconds
from AI.nlp.text_cleaner import normalize_transcript

logger = logging.getLogger("ai_interview_analyzer.transcription_pipeline")


def run_transcription(audio_path: str, raw_dir: str, cleaned_dir: str, json_dir: str,
                       base_filename: str, backend: str = "google", model_size: str = "base",
                       models_dir: str = "models/whisper") -> dict:
    """
    Returns:
        {
            "raw_text": str, "cleaned_text": str, "language": dict,
            "pause_stats": dict, "duration_seconds": float,
            "raw_path": str, "cleaned_path": str, "json_path": str
        }
    """
    result = transcribe_audio(audio_path, backend=backend, model_size=model_size, models_dir=models_dir)
    # transcription backends may raise or return unexpected structures; guard against failures
    try:
        raw_text = result["text"]
    except Exception:
        logger.exception("Transcription backend failed for %s", audio_path)
        raw_text = ""
    cleaned_text = normalize_transcript(raw_text)

    language_info = detect_language(cleaned_text)
    pause_stats = compute_pause_statistics(audio_path)
    duration_seconds = get_audio_duration_seconds(audio_path)

    raw_path = os.path.join(raw_dir, f"{base_filename}.txt")
    cleaned_path = os.path.join(cleaned_dir, f"{base_filename}.txt")
    json_path = os.path.join(json_dir, f"{base_filename}.json")

    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(cleaned_dir, exist_ok=True)
    os.makedirs(json_dir, exist_ok=True)

    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(raw_text)
    with open(cleaned_path, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "raw_text": raw_text,
            "cleaned_text": cleaned_text,
            "engine": result.get("engine"),
            "segments": result.get("segments", []),
            "language": language_info,
            "pause_stats": pause_stats,
            "duration_seconds": duration_seconds,
        }, f, indent=2)

    logger.info("Transcription pipeline complete for %s", base_filename)

    return {
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "language": language_info,
        "pause_stats": pause_stats,
        "duration_seconds": duration_seconds,
        "raw_path": raw_path,
        "cleaned_path": cleaned_path,
        "json_path": json_path,
    }

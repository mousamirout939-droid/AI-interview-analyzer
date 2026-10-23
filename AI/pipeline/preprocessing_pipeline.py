"""
preprocessing_pipeline.py
===========================
Stage 1 pipeline: takes an uploaded media file (video or audio) and
produces a clean, noise-reduced WAV file ready for transcription.
"""

import os
import logging

from AI.speech.audio_extractor import extract_audio_from_video, is_audio_only
from AI.speech.audio_preprocessing import preprocess_audio
from AI.speech.noise_reduction import reduce_noise

logger = logging.getLogger("ai_interview_analyzer.preprocessing_pipeline")


def run_preprocessing(source_path: str, extracted_dir: str, cleaned_dir: str,
                       noise_removed_dir: str, base_filename: str) -> dict:
    """
    Args:
        source_path: path to the uploaded video/audio file.
        extracted_dir, cleaned_dir, noise_removed_dir: output folders (config.py).
        base_filename: filename (without extension) to use for outputs.

    Returns:
        {"extracted": path, "cleaned": path, "noise_removed": path}
    """
    extracted_path = os.path.join(extracted_dir, f"{base_filename}.wav")

    if is_audio_only(source_path):
        preprocess_audio(source_path, extracted_path)
    else:
        extract_audio_from_video(source_path, extracted_path)

    cleaned_path = os.path.join(cleaned_dir, f"{base_filename}.wav")
    preprocess_audio(extracted_path, cleaned_path)

    noise_removed_path = os.path.join(noise_removed_dir, f"{base_filename}.wav")
    reduce_noise(cleaned_path, noise_removed_path)

    logger.info("Preprocessing pipeline complete for %s", base_filename)
    return {
        "extracted": extracted_path,
        "cleaned": cleaned_path,
        "noise_removed": noise_removed_path,
    }

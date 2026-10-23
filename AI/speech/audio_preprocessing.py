"""
audio_preprocessing.py
=======================
Normalizes raw extracted audio so downstream noise-reduction and
transcription stages receive consistent input: fixed sample rate, mono
channel, and normalized loudness.
"""

import os
import logging
from pydub import AudioSegment, effects

logger = logging.getLogger("ai_interview_analyzer.audio_preprocessing")


def preprocess_audio(input_path: str, output_path: str, sample_rate: int = 16000) -> str:
    """
    Normalize an audio file's volume, sample rate, and channel count.

    Args:
        input_path: Path to raw audio file.
        output_path: Path to write the preprocessed audio file.
        sample_rate: Target sample rate in Hz.

    Returns:
        output_path
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    audio = AudioSegment.from_file(input_path)
    audio = audio.set_frame_rate(sample_rate).set_channels(1)
    audio = effects.normalize(audio)  # normalize peak loudness

    audio.export(output_path, format="wav")
    logger.info("Preprocessed audio %s -> %s", input_path, output_path)
    return output_path


def trim_silence_edges(input_path: str, output_path: str, silence_thresh_db: int = -40) -> str:
    """Trim leading/trailing silence from an audio clip."""
    audio = AudioSegment.from_file(input_path)

    def _detect_leading_silence(sound, silence_threshold=silence_thresh_db, chunk_size=10):
        trim_ms = 0
        while trim_ms < len(sound):
            chunk = sound[trim_ms:trim_ms + chunk_size]
            if chunk.dBFS > silence_threshold or chunk.dBFS == float("-inf"):
                if chunk.dBFS > silence_threshold:
                    break
            trim_ms += chunk_size
        return trim_ms

    start_trim = _detect_leading_silence(audio)
    end_trim = _detect_leading_silence(audio.reverse())
    duration = len(audio)
    trimmed = audio[start_trim: duration - end_trim] if duration - end_trim > start_trim else audio

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    trimmed.export(output_path, format="wav")
    return output_path

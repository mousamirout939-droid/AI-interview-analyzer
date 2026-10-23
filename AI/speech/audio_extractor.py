"""
audio_extractor.py
===================
Extracts a mono, 16kHz WAV audio track from an uploaded video file using
ffmpeg (via the `pydub` wrapper). This is the first stage of the speech
pipeline: video in, clean raw audio out.
"""

import os
import logging
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

logger = logging.getLogger("ai_interview_analyzer.audio_extractor")

TARGET_SAMPLE_RATE = 16000
TARGET_CHANNELS = 1


class AudioExtractionError(Exception):
    """Raised when audio cannot be extracted from the source media file."""


def extract_audio_from_video(video_path: str, output_path: str) -> str:
    """
    Extract audio from a video file and save as a normalized WAV file.

    Args:
        video_path: Path to the source video (mp4, mov, avi, mkv, webm...).
        output_path: Destination path for the extracted .wav file.

    Returns:
        The output_path on success.

    Raises:
        AudioExtractionError: if the file cannot be read or decoded.
    """
    if not os.path.exists(video_path):
        raise AudioExtractionError(f"Source video not found: {video_path}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        audio = AudioSegment.from_file(video_path)
        audio = audio.set_frame_rate(TARGET_SAMPLE_RATE).set_channels(TARGET_CHANNELS)
        audio.export(output_path, format="wav")
        logger.info("Extracted audio from %s -> %s", video_path, output_path)
        return output_path
    except CouldntDecodeError as exc:
        raise AudioExtractionError(
            f"Could not decode audio from '{video_path}'. Ensure ffmpeg is installed "
            f"and the file is a valid media container."
        ) from exc
    except Exception as exc:  # pragma: no cover - defensive
        raise AudioExtractionError(f"Unexpected error extracting audio: {exc}") from exc


def get_audio_duration_seconds(audio_path: str) -> float:
    """Return duration of an audio file in seconds."""
    audio = AudioSegment.from_file(audio_path)
    return len(audio) / 1000.0


def is_audio_only(file_path: str) -> bool:
    """Heuristic: return True if a file extension indicates audio rather than video."""
    ext = os.path.splitext(file_path)[1].lower().lstrip(".")
    return ext in {"wav", "mp3", "m4a", "flac", "ogg"}

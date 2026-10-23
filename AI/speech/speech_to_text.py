"""
speech_to_text.py
===================
Transcribes interview audio into text. Supports two backends selected via
config.TRANSCRIPTION_BACKEND:

  * "google"  - uses SpeechRecognition's Google Web Speech API client.
                Lightweight, no model download, works out of the box.
  * "whisper" - uses faster-whisper for fully offline transcription with
                word-level timestamps and higher accuracy. Requires the
                optional dependency (see whisper_loader.py).

Both backends return a normalized result dict so the rest of the pipeline
never needs to know which engine produced the transcript.
"""

import logging
import speech_recognition as sr

from AI.speech.whisper_loader import load_whisper_model, is_whisper_available, WhisperUnavailableError

logger = logging.getLogger("ai_interview_analyzer.speech_to_text")


class TranscriptionError(Exception):
    """Raised when audio cannot be transcribed by any available backend."""


def _transcribe_with_google(audio_path: str) -> dict:
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
        return {"text": text, "segments": [], "engine": "google", "confidence": None}
    except sr.UnknownValueError:
        return {"text": "", "segments": [], "engine": "google", "confidence": 0.0}
    except sr.RequestError as exc:
        raise TranscriptionError(f"Google Speech API request failed: {exc}") from exc


def _transcribe_with_whisper(audio_path: str, model_size: str = "base", models_dir: str = "models/whisper") -> dict:
    model = load_whisper_model(model_size=model_size, models_dir=models_dir)
    segments_iter, info = model.transcribe(audio_path, beam_size=5)

    segments = []
    full_text_parts = []
    for seg in segments_iter:
        segments.append({"start": seg.start, "end": seg.end, "text": seg.text.strip()})
        full_text_parts.append(seg.text.strip())

    return {
        "text": " ".join(full_text_parts).strip(),
        "segments": segments,
        "engine": "whisper",
        "confidence": getattr(info, "language_probability", None),
    }


def transcribe_audio(audio_path: str, backend: str = "google", model_size: str = "base",
                      models_dir: str = "models/whisper") -> dict:
    """
    Transcribe an audio file to text.

    Args:
        audio_path: path to a WAV/FLAC/AIFF audio file.
        backend: "google" or "whisper".
        model_size: whisper model size (ignored for google backend).
        models_dir: local cache directory for whisper weights.

    Returns:
        dict with keys: text, segments, engine, confidence
    """
    backend = (backend or "google").lower()

    if backend == "whisper":
        if not is_whisper_available():
            logger.warning("Whisper backend requested but not installed; falling back to Google backend.")
            return _transcribe_with_google(audio_path)
        try:
            return _transcribe_with_whisper(audio_path, model_size=model_size, models_dir=models_dir)
        except WhisperUnavailableError:
            logger.warning("Whisper unavailable at runtime; falling back to Google backend.")
            return _transcribe_with_google(audio_path)

    return _transcribe_with_google(audio_path)

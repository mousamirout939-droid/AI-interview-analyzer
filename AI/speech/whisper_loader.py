"""
whisper_loader.py
===================
Optional loader for an offline OpenAI-Whisper style transcription backend.

Whisper models are large (tens to hundreds of MB) and require the optional
`faster-whisper` (or `openai-whisper`) package plus a torch runtime. To keep
the base install lightweight, this module lazily imports the dependency and
degrades gracefully (raising WhisperUnavailableError) if it isn't installed,
so the rest of the app can fall back to the `google` SpeechRecognition
backend configured in TRANSCRIPTION_BACKEND.
"""

import logging
import os

logger = logging.getLogger("ai_interview_analyzer.whisper_loader")

_model_cache = {}


class WhisperUnavailableError(Exception):
    """Raised when the whisper backend is requested but not installed."""


def is_whisper_available() -> bool:
    try:
        import faster_whisper  # noqa: F401
        return True
    except ImportError:
        return False


def load_whisper_model(model_size: str = "base", models_dir: str = "models/whisper"):
    """
    Load (and cache) a faster-whisper model instance.

    Args:
        model_size: one of tiny, base, small, medium, large-v3
        models_dir: local directory used to cache downloaded model weights

    Returns:
        A loaded WhisperModel instance.

    Raises:
        WhisperUnavailableError if the optional dependency isn't installed.
    """
    if model_size in _model_cache:
        return _model_cache[model_size]

    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise WhisperUnavailableError(
            "faster-whisper is not installed. Install it with "
            "'pip install faster-whisper' to enable offline transcription, "
            "or set TRANSCRIPTION_BACKEND=google to use the default backend."
        ) from exc

    os.makedirs(models_dir, exist_ok=True)
    logger.info("Loading whisper model '%s' (this may take a while on first run)...", model_size)
    model = WhisperModel(model_size, download_root=models_dir, compute_type="int8")
    _model_cache[model_size] = model
    return model

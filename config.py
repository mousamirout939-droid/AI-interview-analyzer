"""
config.py
=========
Central configuration for the AI Interview Analyzer application.

Configuration is environment-driven (see .env.example) and split into
Development / Testing / Production profiles so the same codebase can be
safely deployed to different environments.
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


def _bool(value, default=False):
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


class BaseConfig:
    """Shared configuration across all environments."""

    # --- Core Flask ---
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    DEBUG = False
    TESTING = False

    # --- Database ---
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'interview_analyzer.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    # --- Uploads ---
    BASE_UPLOAD_FOLDER = os.path.join(BASE_DIR, os.environ.get("UPLOAD_FOLDER", "uploads"))
    VIDEO_ORIGINAL_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "videos", "original")
    VIDEO_COMPRESSED_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "videos", "compressed")
    VIDEO_THUMBNAIL_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "videos", "thumbnails")
    AUDIO_EXTRACTED_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "audio", "extracted")
    AUDIO_CLEANED_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "audio", "cleaned")
    AUDIO_NOISE_REMOVED_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "audio", "noise_removed")
    TRANSCRIPT_RAW_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "transcripts", "raw")
    TRANSCRIPT_CLEANED_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "transcripts", "cleaned")
    TRANSCRIPT_JSON_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "transcripts", "json")
    TEMP_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "temp")
    REPORT_FOLDER = os.path.join(BASE_DIR, "data", "processed", "scores")

    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH_MB", 250)) * 1024 * 1024
    ALLOWED_VIDEO_EXTENSIONS = {"mp4", "mov", "avi", "mkv", "webm"}
    ALLOWED_AUDIO_EXTENSIONS = {"wav", "mp3", "m4a", "flac", "ogg"}

    # --- AI / Speech ---
    TRANSCRIPTION_BACKEND = os.environ.get("TRANSCRIPTION_BACKEND", "google")
    WHISPER_MODEL_SIZE = os.environ.get("WHISPER_MODEL_SIZE", "base")
    MODELS_DIR = os.path.join(BASE_DIR, "models")
    DATASETS_DIR = os.path.join(BASE_DIR, "datasets")

    # --- Auth / Security ---
    PASSWORD_MIN_LENGTH = int(os.environ.get("PASSWORD_MIN_LENGTH", 8))
    SESSION_COOKIE_SECURE = _bool(os.environ.get("SESSION_COOKIE_SECURE"), False)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    REMEMBER_COOKIE_DURATION = timedelta(days=14)

    # --- Pagination ---
    ITEMS_PER_PAGE = int(os.environ.get("ITEMS_PER_PAGE", 10))

    # --- Theme (exposed to templates via context processor) ---
    THEME = {
        "primary": "#B497D6",       # lavender
        "primary_dark": "#8E6FB0",  # deep lavender
        "secondary": "#F7C6D9",     # light pink
        "secondary_light": "#FDEAF2",  # pale pink
        "accent": "#6FCF97",        # green
        "accent_dark": "#3FA66E",   # deep green
        "background": "#FBF7FC",
        "surface": "#FFFFFF",
        "text": "#3A2E4D",
        "muted": "#8A7A9B",
    }

    @staticmethod
    def init_app(app):
        """Hook for subclasses / factory to run extra setup."""
        for folder in [
            app.config["BASE_UPLOAD_FOLDER"],
            app.config["VIDEO_ORIGINAL_FOLDER"],
            app.config["VIDEO_COMPRESSED_FOLDER"],
            app.config["VIDEO_THUMBNAIL_FOLDER"],
            app.config["AUDIO_EXTRACTED_FOLDER"],
            app.config["AUDIO_CLEANED_FOLDER"],
            app.config["AUDIO_NOISE_REMOVED_FOLDER"],
            app.config["TRANSCRIPT_RAW_FOLDER"],
            app.config["TRANSCRIPT_CLEANED_FOLDER"],
            app.config["TRANSCRIPT_JSON_FOLDER"],
            app.config["TEMP_FOLDER"],
            app.config["REPORT_FOLDER"],
            os.path.join(BASE_DIR, "instance"),
            os.path.join(BASE_DIR, "logs"),
        ]:
            os.makedirs(folder, exist_ok=True)


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    DEBUG = False
    SESSION_COOKIE_SECURE = True


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config():
    env = os.environ.get("FLASK_ENV", "development")
    return config_by_name.get(env, DevelopmentConfig)

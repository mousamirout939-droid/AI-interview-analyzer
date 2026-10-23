"""
download_models.py
=====================
Pre-downloads NLTK corpora and (optionally) a Whisper model so the first
real user request doesn't pay the download cost. Run this once after
installing dependencies, especially in production/CI environments.

Usage:
    python scripts/download_models.py
    python scripts/download_models.py --whisper base
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def download_nltk_data(target_dir: str):
    import nltk
    os.makedirs(target_dir, exist_ok=True)
    if target_dir not in nltk.data.path:
        nltk.data.path.insert(0, target_dir)

    packages = ["punkt", "punkt_tab", "averaged_perceptron_tagger",
                "averaged_perceptron_tagger_eng", "wordnet", "omw-1.4", "stopwords"]
    for pkg in packages:
        try:
            nltk.download(pkg, download_dir=target_dir, quiet=True)
            print(f"Downloaded NLTK package: {pkg}")
        except Exception as exc:
            print(f"Skipped NLTK package '{pkg}': {exc}")


def download_whisper_model(model_size: str, target_dir: str):
    try:
        from AI.speech.whisper_loader import load_whisper_model
        load_whisper_model(model_size=model_size, models_dir=target_dir)
        print(f"Whisper model '{model_size}' downloaded/cached at {target_dir}")
    except Exception as exc:
        print(f"Could not download whisper model (optional dependency): {exc}")


def main():
    parser = argparse.ArgumentParser(description="Pre-download AI models/corpora.")
    parser.add_argument("--whisper", nargs="?", const="base", default=None,
                         help="Also download a whisper model of this size (requires faster-whisper).")
    args = parser.parse_args()

    from config import BaseConfig
    download_nltk_data(os.path.join(BaseConfig.MODELS_DIR, "nltk"))

    if args.whisper:
        download_whisper_model(args.whisper, os.path.join(BaseConfig.MODELS_DIR, "whisper"))


if __name__ == "__main__":
    main()

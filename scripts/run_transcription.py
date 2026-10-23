#!/usr/bin/env python3
"""Advanced runner for the transcription pipeline.

Features:
- directory processing (recursive)
- concurrency (ThreadPoolExecutor)
- optional preprocessing (resample/normalize), trimming, denoising
- whisper backend support with model-size
- optional DB persistence
"""
import argparse
import json
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import shutil

from AI.pipeline.transcription_pipeline import run_transcription

LOG = logging.getLogger("scripts.run_transcription")


def _find_audio_files(path: Path, recursive: bool = False):
    exts = {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".aiff", ".aif"}
    if path.is_file():
        return [path]
    files = []
    if recursive:
        for p in path.rglob("*"):
            if p.suffix.lower() in exts:
                files.append(p)
    else:
        for p in path.iterdir():
            if p.suffix.lower() in exts:
                files.append(p)
    return sorted(files)


def _check_ffmpeg():
    ff = shutil.which("ffmpeg") or shutil.which("avconv")
    if not ff:
        LOG.warning("ffmpeg not found in PATH. Install ffmpeg for robust audio handling.")
    return bool(ff)


def process_file(audio_path: str, base_name: str, backend: str, models_dir: str, model_size: str, out_base: Path,
                 preprocess: bool = False, denoise: bool = False, trim: bool = False):
    raw_dir = out_base / "raw"
    cleaned_dir = out_base / "cleaned"
    json_dir = out_base / "json"
    raw_dir.mkdir(parents=True, exist_ok=True)
    cleaned_dir.mkdir(parents=True, exist_ok=True)
    json_dir.mkdir(parents=True, exist_ok=True)

    try:
        LOG.info("Processing %s", audio_path)

        # Optional preprocessing steps
        working_file = str(audio_path)
        tmp_dir = out_base / "tmp"
        tmp_dir.mkdir(parents=True, exist_ok=True)
        # lazy imports
        from AI.speech.audio_preprocessing import preprocess_audio, trim_silence_edges
        from AI.speech.noise_reduction import denoise_with_backend

        if preprocess:
            pre_out = str(tmp_dir / f"{base_name}.pre.wav")
            working_file = preprocess_audio(working_file, pre_out)
        if trim:
            trim_out = str(tmp_dir / f"{base_name}.trim.wav")
            working_file = trim_silence_edges(working_file, trim_out)
        if denoise:
            den_out = str(tmp_dir / f"{base_name}.den.wav")
            working_file = denoise_with_backend(working_file, den_out)

        result = run_transcription(working_file, str(raw_dir), str(cleaned_dir), str(json_dir), base_name,
                                   backend=backend, model_size=model_size, models_dir=models_dir)
        return {"ok": True, "result": result}
    except Exception as exc:  # pragma: no cover - runtime failures should be caught here
        LOG.exception("Failed processing %s: %s", audio_path, exc)
        return {"ok": False, "error": str(exc)}


def main():
    p = argparse.ArgumentParser(description="Advanced transcription runner")
    p.add_argument("input", help="Path to an audio file or a directory of audio files")
    p.add_argument("--base-name", dest="base_name", default=None, help="Base filename for single-file output")
    p.add_argument("--backend", default="google", choices=("google", "whisper"), help="Transcription backend")
    p.add_argument("--models-dir", default="models/whisper", help="Whisper models directory")
    p.add_argument("--model-size", default="base", help="Whisper model size (tiny, base, small, medium, large-v3)")
    p.add_argument("--preprocess", action="store_true", help="Run audio preprocessing (resample + normalize) before transcription")
    p.add_argument("--denoise", action="store_true", help="Apply noise reduction after preprocessing")
    p.add_argument("--trim", action="store_true", help="Trim silence from the edges of audio before transcription")
    p.add_argument("--out-dir", default=os.path.join("uploads", "transcripts"), help="Base output directory")
    p.add_argument("--save-to-db", action="store_true", help="Save transcript metadata to the app DB if available")
    p.add_argument("--interview-id", type=int, default=None, help="Interview ID to associate with transcript when saving to DB")
    p.add_argument("--recursive", action="store_true", help="Recurse into directories when input is a folder")
    p.add_argument("--workers", type=int, default=1, help="Number of concurrent workers (default 1)")
    p.add_argument("--log-level", default="INFO", help="Logging level")
    args = p.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO),
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    input_path = Path(args.input)
    if not input_path.exists():
        LOG.error("Input not found: %s", input_path)
        sys.exit(2)

    _check_ffmpeg()

    # Hugging Face token improves download reliability/rate limits for whisper models
    hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    if args.backend == "whisper" and not hf_token:
        LOG.warning("No HF_TOKEN set — downloads may be slower or rate-limited. Set HF_TOKEN env var to improve reliability.")

    audio_files = _find_audio_files(input_path, recursive=args.recursive)
    if not audio_files:
        LOG.error("No audio files found in: %s", input_path)
        sys.exit(2)

    out_base = Path(args.out_dir)
    out_base.mkdir(parents=True, exist_ok=True)

    tasks = []
    for pth in audio_files:
        base_name = args.base_name or pth.stem
        tasks.append((pth, base_name))

    results = []
    if args.workers > 1:
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futures = {ex.submit(process_file, pth, base, args.backend, args.models_dir, args.model_size, out_base / pth.stem,
                                args.preprocess, args.denoise, args.trim): pth for pth, base in tasks}
            for fut in as_completed(futures):
                results.append(fut.result())
    else:
        for pth, base in tasks:
            results.append(process_file(pth, base, args.backend, args.models_dir, args.model_size, out_base / pth.stem,
                                        args.preprocess, args.denoise, args.trim))

    successful = sum(1 for r in results if r.get("ok"))
    LOG.info("Processing complete: %d/%d succeeded", successful, len(results))
    print(json.dumps({"total": len(results), "succeeded": successful}, indent=2))

    # Optionally persist to DB
    if args.save_to_db:
        from AI.pipeline.persistence import save_transcript
        saved = 0
        for r in results:
            if r.get("ok"):
                ok = save_transcript(r.get("result"), interview_id=args.interview_id)
                if ok:
                    saved += 1
        LOG.info("Persisted %d transcripts to DB", saved)


if __name__ == "__main__":
    main()

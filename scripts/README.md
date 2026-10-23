Transcription Scripts
=====================

This folder contains helper scripts to run and test the transcription pipeline.

Run the advanced runner:

```bash
# Process a single file
python scripts/run_transcription.py /path/to/audio.wav --model-size base --backend google

# Process a directory recursively with 4 workers
python scripts/run_transcription.py uploads/audio --recursive --workers 4 --backend whisper --model-size base
```

Notes and prerequisites
- Install Python dependencies from `requirements.txt`.
- For robust audio handling, install `ffmpeg` and add it to your PATH.
- For Whisper offline transcription, install the optional dependencies:

```bash
pip install faster-whisper ctranslate2 onnxruntime av
```

- Set a Hugging Face token in `HF_TOKEN` to avoid unauthenticated rate limits when downloading models:

```bash
# PowerShell
$env:HF_TOKEN = "<your_token>"
# Linux/macOS
export HF_TOKEN="<your_token>"
```

Testing
- Generate a short silent WAV for testing:

```bash
python scripts/generate_silence.py
```

- Run tests:

```bash
pytest -q
```

Tips
- Use `--model-size` to control memory and accuracy trade-offs (tiny, base, small, medium, large-v3).
- The first Whisper run will download model weights and may take a while.

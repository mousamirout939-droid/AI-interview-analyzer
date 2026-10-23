import wave
import os
from AI.pipeline.transcription_pipeline import run_transcription


def _make_silence(path: str, duration_s: float = 1.0, rate: int = 16000):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    nframes = int(duration_s * rate)
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(b'\x00\x00' * nframes)


def test_transcription_pipeline_basic(tmp_path):
    audio_path = tmp_path / "test_silence.wav"
    _make_silence(str(audio_path))

    out_base = tmp_path / "out"
    raw_dir = out_base / "raw"
    cleaned_dir = out_base / "cleaned"
    json_dir = out_base / "json"

    res = run_transcription(str(audio_path), str(raw_dir), str(cleaned_dir), str(json_dir), "test_silence")

    assert isinstance(res, dict)
    assert abs(res.get("duration_seconds", 0) - 1.0) < 0.1
    assert os.path.exists(res.get("json_path"))
    assert os.path.exists(res.get("raw_path"))
    assert os.path.exists(res.get("cleaned_path"))

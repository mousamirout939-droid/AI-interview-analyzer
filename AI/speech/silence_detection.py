"""
silence_detection.py
=====================
Detects silent segments in interview audio. Used to measure pause
patterns (a key input to the fluency/confidence scoring models) and to
optionally strip dead air before transcription.
"""

from pydub import AudioSegment
from pydub.silence import detect_silence, detect_nonsilent


def find_silent_segments(audio_path: str, min_silence_len: int = 500, silence_thresh: int = -35):
    """
    Return a list of (start_ms, end_ms) tuples for silent segments.

    Args:
        audio_path: Path to audio file.
        min_silence_len: Minimum length (ms) to be considered silence.
        silence_thresh: dBFS threshold below which audio is treated as silent.
    """
    audio = AudioSegment.from_file(audio_path)
    thresh = silence_thresh if silence_thresh is not None else audio.dBFS - 16
    return detect_silence(audio, min_silence_len=min_silence_len, silence_thresh=thresh)


def find_speaking_segments(audio_path: str, min_silence_len: int = 400, silence_thresh: int = -35):
    """Return a list of (start_ms, end_ms) tuples for non-silent (speaking) segments."""
    audio = AudioSegment.from_file(audio_path)
    thresh = silence_thresh if silence_thresh is not None else audio.dBFS - 16
    return detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=thresh)


def compute_pause_statistics(audio_path: str) -> dict:
    """
    Compute pause-related statistics used by the fluency scorer:
    total pause time, number of pauses, average pause length, and
    speaking ratio (fraction of the recording that contains speech).
    """
    audio = AudioSegment.from_file(audio_path)
    total_duration_ms = len(audio)

    silent_segments = find_silent_segments(audio_path)
    total_pause_ms = sum(end - start for start, end in silent_segments)
    num_pauses = len(silent_segments)
    avg_pause_ms = (total_pause_ms / num_pauses) if num_pauses else 0.0
    speaking_ratio = (
        1 - (total_pause_ms / total_duration_ms) if total_duration_ms else 0.0
    )

    return {
        "total_duration_ms": total_duration_ms,
        "total_pause_ms": total_pause_ms,
        "num_pauses": num_pauses,
        "avg_pause_ms": round(avg_pause_ms, 2),
        "speaking_ratio": round(max(0.0, min(1.0, speaking_ratio)), 3),
    }

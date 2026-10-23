"""
noise_reduction.py
====================
Lightweight noise reduction for interview audio recordings.

A full spectral-subtraction / deep-learning denoiser (e.g. RNNoise, DeepFilterNet)
can be swapped in via the `denoise_with_backend` hook. By default we apply a
dependency-light high-pass filter + gain compression using pydub, which
removes low-frequency hum and normalizes dynamic range without requiring
extra native binaries.
"""

import os
import logging
from pydub import AudioSegment

logger = logging.getLogger("ai_interview_analyzer.noise_reduction")


def reduce_noise(input_path: str, output_path: str, high_pass_hz: int = 100) -> str:
    """
    Apply a high-pass filter and dynamic range compression to suppress
    background hum/hiss commonly present in webcam/microphone recordings.

    Args:
        input_path: Path to the (preprocessed) input audio.
        output_path: Path to write the noise-reduced audio.
        high_pass_hz: Cutoff frequency for the high-pass filter.

    Returns:
        output_path
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    audio = AudioSegment.from_file(input_path)
    filtered = audio.high_pass_filter(high_pass_hz)
    # Gentle compression: reduce peak volume spikes then normalize
    compressed = filtered.apply_gain(-filtered.max_dBFS + 3 if filtered.max_dBFS > -3 else 0)

    compressed.export(output_path, format="wav")
    logger.info("Noise reduced %s -> %s", input_path, output_path)
    return output_path


def denoise_with_backend(input_path: str, output_path: str, backend: str = "builtin") -> str:
    """
    Pluggable entry point for swapping in a more advanced denoiser.
    Currently only 'builtin' (this module's high-pass filter) is implemented;
    additional backends (e.g. 'rnnoise', 'deepfilternet') can be registered
    here without changing calling code.
    """
    if backend == "builtin":
        return reduce_noise(input_path, output_path)
    raise NotImplementedError(f"Noise reduction backend '{backend}' is not available.")

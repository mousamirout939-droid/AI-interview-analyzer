#!/usr/bin/env python3
"""Generate a 1-second silent WAV file for testing."""
import os
import wave


def generate_silence(path: str, duration_s: float = 1.0, rate: int = 16000):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    nframes = int(duration_s * rate)
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit samples
        wf.setframerate(rate)
        wf.writeframes(b'\x00\x00' * nframes)


if __name__ == '__main__':
    out = os.path.join('uploads', 'audio', 'test_silence.wav')
    generate_silence(out)
    print(out)

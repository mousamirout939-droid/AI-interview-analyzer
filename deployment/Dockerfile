# ============================================================
# AI Interview Analyzer — Production Dockerfile
# ============================================================
FROM python:3.11-slim

# System dependencies: ffmpeg for audio/video processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# Pre-download NLTK corpora at build time so runtime requests are fast
RUN python scripts/download_models.py || true

RUN mkdir -p instance logs \
    uploads/videos/original uploads/videos/compressed uploads/videos/thumbnails \
    uploads/audio/extracted uploads/audio/cleaned uploads/audio/noise_removed \
    uploads/transcripts/raw uploads/transcripts/cleaned uploads/transcripts/json uploads/temp \
    data/processed/scores

ENV FLASK_ENV=production \
    PYTHONUNBUFFERED=1 \
    PORT=5000

EXPOSE 5000

CMD ["gunicorn", "-c", "deployment/gunicorn.conf.py", "app:app"]

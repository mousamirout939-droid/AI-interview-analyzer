# 🌿 AI Interview Analyzer

A full-stack, production-structured Flask application that analyzes practice
interview recordings (video or audio) and returns detailed, AI-driven
feedback: speech transcription, grammar/vocabulary/sentiment analysis, six
weighted performance scores, strengths/weaknesses, improvement tips, a
downloadable PDF report, and a candidate leaderboard.

Theme: **lavender + light pink + sage green** ("Botanical Study" palette) —
see `static/css/theme.css`.

---

## ✨ Features

- **Authentication** — secure registration/login (salted password hashing via Werkzeug), session management via Flask-Login, role-based access (candidate/admin).
- **Upload pipeline** — upload a video or audio recording; the app extracts, cleans, and denoises the audio automatically.
- **Speech-to-text** — pluggable transcription backend: lightweight Google Web Speech API (default, no downloads) or fully offline `faster-whisper` (optional).
- **NLP analysis** — tokenization, stopword removal, stemming/lemmatization, POS tagging, keyword & technical-term extraction, grammar checking, filler-word detection.
- **Sentiment & emotion analysis** — polarity, subjectivity, and a transparent, lexicon-based emotion model (confidence, nervousness, enthusiasm, calmness).
- **Scoring engine** — six dimension scores (Fluency, Confidence, Grammar, Vocabulary, Technical Depth, Communication) combined into a weighted overall score with a verdict.
- **Recommendations** — auto-generated strengths, weaknesses, actionable improvement tips, and narrative feedback.
- **Reports** — themed HTML report view + downloadable PDF export (ReportLab).
- **Leaderboard** — ranks all candidates by overall score with percentile standing.
- **Dashboard & history** — stats overview, paginated interview history.
- **Resume roadmap & interview preparation** — privately analyze a PDF, DOCX, or TXT resume to identify listed skills, choose or infer a role track, see prioritized study topics linked to the learning guides, and practise role-specific interview questions. Resume files are processed in memory and are not saved.
- **Learning** — public, browsable original guides for Python, JavaScript, HTML/CSS, Java, C, C++, C#, Rust, PHP, SQL, and TypeScript, with beginner, intermediate, and advanced notes and examples.
- **Production-ready plumbing** — app factory pattern, blueprints, service/controller separation, structured logging, error handlers, Docker/Gunicorn/Render deployment configs, and a pytest test suite.

---

## 🗂 Project Structure

```
AI-interview-analyzer/
├── app.py                   # Entry point
├── config.py                 # Environment-driven configuration + theme colors
├── requirements.txt
├── .env.example
├── APP/                       # Web application layer
│   ├── routes/                # Flask blueprints (thin, URL wiring only)
│   ├── controllers/            # Request handling logic
│   ├── services/                # Business logic (auth, storage, interviews, ranking, reports)
│   ├── database/                 # SQLAlchemy models (User, Interview, Transcript, Analysis, Report, Ranking)
│   ├── middleware/                # Auth guards, upload validation, error handlers
│   └── utils/                      # Validators, security, file utils, helpers, logging
├── AI/                        # AI / ML pipeline (framework-agnostic, no Flask imports)
│   ├── speech/                 # Audio extraction, preprocessing, noise reduction, silence detection, transcription
│   ├── nlp/                     # Tokenizer, stopwords, stemming, lemmatization, POS tagging, keywords, grammar, fillers
│   ├── sentiment/                 # Polarity, subjectivity, emotion analysis
│   ├── scoring/                    # Per-dimension scorers, overall score, candidate ranker
│   ├── recommendation/              # Strengths/weaknesses detection, tips, feedback, summary
│   └── pipeline/                     # Stage orchestrators + end-to-end complete_pipeline
├── evaluation/                # Metrics, evaluator, benchmarking, performance snapshot
├── templates/                  # Jinja2 templates (themed UI)
├── static/css, static/js       # Theme CSS + progressive-enhancement JS
├── APP/services/learning_content.py # Original programming learning notes and code examples
├── datasets/                    # Stopwords, filler words, sentiment word lists, technical keyword bank, sample data
├── models/                       # Local cache for downloaded NLTK/Whisper models (gitignored contents)
├── uploads/                       # Runtime media/transcript storage (gitignored contents)
├── data/processed/                 # Generated score/sentiment artifacts (gitignored contents)
├── scripts/                    # initialize_database, create_admin, clean_uploads, backup_database, download_models
├── tests/                       # pytest suite covering auth, NLP, sentiment, scoring, pipeline, DB, reports, uploads
└── deployment/                  # Dockerfile, docker-compose.yml, gunicorn.conf.py, render.yaml
```

---

## 🚀 Quick Start (local development)

**Prerequisites:** Python 3.10+, `ffmpeg` installed and on your PATH (required for audio extraction).

```bash
# 1. Clone / unzip the project, then enter it
cd AI-interview-analyzer

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env            # adjust values as needed

# 5. Pre-download NLP corpora (recommended, avoids first-request delay)
python scripts/download_models.py

# 6. Initialize the database
python scripts/initialize_database.py

# 7. (Optional) create an admin account
python scripts/create_admin.py

# 8. Run the app
python app.py
```

Visit **http://localhost:5000**.

---

## 🐳 Run with Docker

```bash
cd deployment
docker compose up --build
```

The app will be available at **http://localhost:5000**. Data persists in Docker named volumes (`app-instance`, `app-uploads`, `app-logs`).

---

## 🧪 Running Tests

```bash
pytest -v
```

Tests use an in-memory SQLite database (`TestingConfig`) and cover authentication, NLP utilities, sentiment analysis, scoring math, the text-based pipeline, database models, PDF report generation, and upload validation.

## 🧭 Resume Roadmap & Interview Preparation

Sign in and choose **Resume roadmap** to upload a text-based PDF, DOCX, or TXT resume (up to 5 MB). You can select a target role or let the site infer a starting track from resume keywords. The results highlight detected skills, role-aligned areas to study, and links to matching programming guides. Interview practice is grouped into resume/project, technical, aptitude/problem-solving, and behavioral questions; technical prompts are selected from skills detected in the resume. These are rule-based practice suggestions, not a scored aptitude assessment, hiring decision, or substitute for professional career advice. Resume contents are processed for the request and not stored.

---

## 🔌 Swapping the Transcription Backend

By default, `TRANSCRIPTION_BACKEND=google` uses `SpeechRecognition`'s Google Web Speech client — zero model downloads, works out of the box, but requires internet access at request time.

For a fully offline, higher-accuracy alternative:

```bash
pip install faster-whisper
```

Then set in `.env`:
```
TRANSCRIPTION_BACKEND=whisper
WHISPER_MODEL_SIZE=base   # tiny | base | small | medium | large-v3
```

The pipeline automatically falls back to the Google backend if `faster-whisper` isn't installed, so the app never hard-fails due to a missing optional dependency.

---

## 📊 How Scoring Works

Each interview recording flows through five pipeline stages
(`AI/pipeline/complete_pipeline.py`):

1. **Preprocessing** — extract audio → normalize → reduce noise.
2. **Transcription** — speech-to-text + language detection + pause statistics.
3. **NLP analysis** — tokenize, extract keywords, check grammar, detect filler words, run sentiment/emotion analysis.
4. **Scoring** — six dimension scorers each return a 0–100 score:
   - **Fluency** — speaking pace, pause patterns, filler-word rate.
   - **Confidence** — emotion-model confidence/calmness/nervousness signals.
   - **Grammar** — rule-based grammar issue rate per sentence.
   - **Vocabulary** — lexical diversity + content-word density.
   - **Technical Depth** — weighted domain keyword coverage (`datasets/technical_keywords.csv`).
   - **Communication** — sentence structure + grammar quality.

   These combine into a weighted **overall score** (see `DEFAULT_WEIGHTS` in `AI/scoring/overall_score.py`).
5. **Reporting** — strengths/weaknesses detection, tailored improvement tips, narrative feedback, and a persisted summary used by the dashboard, report view, and PDF export.

---

## 🔒 Security Notes for Production

- Set a strong, random `SECRET_KEY` (never reuse the development default).
- Set `SESSION_COOKIE_SECURE=True` when serving over HTTPS (already default in `ProductionConfig`).
- Swap SQLite for Postgres/MySQL via `DATABASE_URL` for concurrent production traffic.
- Interview processing currently runs synchronously in the request/response cycle for simplicity; for high-throughput deployments, move `APP.services.interview_service.process_interview` into a background worker (Celery, RQ, or Dramatiq) queued from the upload endpoint.
- Review and rotate the bootstrap `ADMIN_PASSWORD` immediately after first login.

---

## 📄 License

MIT — see `LICENSE`.

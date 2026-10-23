"""Optional persistence helpers for saving transcription results to the app DB.

These helpers try to import the application's DB and models; if the web
application isn't available in the execution environment they become no-ops
so the transcription pipeline can still run standalone.
"""
import logging

logger = logging.getLogger("ai_interview_analyzer.persistence")


def save_transcript(result: dict, interview_id: int | None = None) -> bool:
    """Attempt to save a transcript record to the application's database.

    Returns True if the record was saved, False otherwise.
    """
    # If no interview_id provided, we'll create a placeholder interview (and user) so
    # the transcript can be associated with a record. This makes the persistence
    # behavior useful for CLI runs and demos.

    try:
        # Import lazily to avoid requiring Flask app in pure CLI runs
        from APP.database.database import db
        from APP.database.transcript_model import Transcript
        from APP.database.interview_model import Interview
        from APP.database.user_model import User
        from APP import create_app
        from config import get_config

        app = create_app(get_config())
        with app.app_context():
            # Ensure interview exists; if not, create a placeholder user and interview
            interview = None
            if interview_id:
                interview = db.session.get(Interview, interview_id)

            if not interview:
                # Ensure at least one user exists or create a placeholder
                user = db.session.execute(db.select(User).limit(1)).scalar_one_or_none()
                if not user:
                    user = User(full_name="Auto User", email="auto@example.com")
                    user.set_password("changeme")
                    db.session.add(user)
                    db.session.flush()

                interview = Interview(
                    user_id=user.id,
                    title="Auto-generated interview",
                    original_filename=result.get("raw_path") or "",
                    stored_filename=result.get("raw_path") or "",
                    file_type="audio",
                )
                db.session.add(interview)
                db.session.flush()

            tr = db.session.execute(
                db.select(Transcript).filter_by(interview_id=interview.id)
            ).scalar_one_or_none()

            if tr is None:
                tr = Transcript(
                    interview_id=interview.id,
                    raw_text=result.get("raw_text"),
                    cleaned_text=result.get("cleaned_text"),
                    language_code=(result.get("language", {}).get("language") if result.get("language") else None),
                    language_confidence=(result.get("language", {}).get("confidence") if result.get("language") else None),
                    transcription_engine=result.get("engine") or result.get("language", {}).get("engine"),
                    raw_path=result.get("raw_path"),
                    cleaned_path=result.get("cleaned_path"),
                    json_path=result.get("json_path"),
                )
                db.session.add(tr)
            else:
                tr.raw_text = result.get("raw_text")
                tr.cleaned_text = result.get("cleaned_text")
                tr.language_code = (result.get("language", {}).get("language") if result.get("language") else None)
                tr.language_confidence = (result.get("language", {}).get("confidence") if result.get("language") else None)
                tr.transcription_engine = result.get("engine") or result.get("language", {}).get("engine")
                tr.raw_path = result.get("raw_path")
                tr.cleaned_path = result.get("cleaned_path")
                tr.json_path = result.get("json_path")

            db.session.commit()
            logger.info("Saved transcript for interview %s to DB (id=%s)", interview.id, tr.id)
            return True
    except Exception as exc:  # pragma: no cover - optional behavior
        logger.exception("Failed to save transcript to DB: %s", exc)
        return False

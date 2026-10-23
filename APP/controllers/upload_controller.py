"""
upload_controller.py
=======================
Handles the interview upload form: validates the incoming file, persists
it to disk, creates the Interview record, and kicks off pipeline
processing (synchronously for this deployment profile).
"""

import logging
from flask import request, redirect, url_for, render_template, flash, current_app
from flask_login import login_required, current_user

from APP.middleware.upload import validate_upload, UploadValidationError
from APP.services.storage_service import store_uploaded_media
from APP.services.interview_service import create_interview, process_interview

logger = logging.getLogger("ai_interview_analyzer.upload_controller")


@login_required
def handle_upload():
    if request.method == "GET":
        return render_template("upload.html")

    file_storage = request.files.get("media_file")
    title = request.form.get("title", "").strip()
    question = request.form.get("question", "").strip()

    try:
        file_type, size_bytes = validate_upload(
            file_storage,
            allowed_video_ext=current_app.config["ALLOWED_VIDEO_EXTENSIONS"],
            allowed_audio_ext=current_app.config["ALLOWED_AUDIO_EXTENSIONS"],
            max_bytes=current_app.config["MAX_CONTENT_LENGTH"],
        )
    except UploadValidationError as exc:
        flash(str(exc), "error")
        return render_template("upload.html"), 400

    stored = store_uploaded_media(file_storage, file_type)

    interview = create_interview(
        user_id=current_user.id,
        title=title or file_storage.filename,
        question=question,
        file_type=file_type,
        original_filename=file_storage.filename,
        stored_filename=stored["stored_filename"],
        size_bytes=stored["size_bytes"],
    )

    try:
        process_interview(interview.id)
        flash("Your interview has been analyzed successfully!", "success")
        return redirect(url_for("analysis.view_analysis", interview_id=interview.id))
    except Exception:
        logger.exception("Pipeline processing failed for interview %s", interview.id)
        flash(
            "We saved your upload, but analysis failed. This can happen with unclear "
            "audio or unsupported formats. You can try uploading again.",
            "error",
        )
        return redirect(url_for("history.view_history"))

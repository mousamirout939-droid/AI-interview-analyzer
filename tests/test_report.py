"""
test_report.py
=================
Tests PDF report generation end-to-end using a fabricated Analysis/Report
so the test doesn't depend on real audio processing.
"""

import os
import json


def _setup_completed_interview(db):
    from APP.database import User, Interview, Analysis, Report

    user = User(full_name="Report User", email="report@example.com", role="candidate")
    user.set_password("Secret123")
    db.session.add(user)
    db.session.commit()

    interview = Interview(
        user_id=user.id, title="Report Test Interview",
        original_filename="a.mp4", stored_filename="b.mp4",
        file_type="video", status="completed",
    )
    db.session.add(interview)
    db.session.commit()

    analysis = Analysis(
        interview_id=interview.id, fluency_score=82, confidence_score=78,
        grammar_score=88, vocabulary_score=74, technical_score=69,
        communication_score=80, overall_score=78.5, verdict="Strong",
        sentiment_label="positive", sentiment_polarity=0.4, dominant_emotion="confidence",
        word_count=120, filler_word_count=90,
    )
    db.session.add(analysis)

    report = Report(
        interview_id=interview.id,
        feedback_text="Great performance overall with strong grammar.",
        strengths_json=json.dumps([{"dimension": "grammar", "score": 88, "description": "Clean grammar"}]),
        weaknesses_json=json.dumps([{"dimension": "technical", "score": 69, "description": "Could improve technical depth"}]),
        tips_json=json.dumps([{"dimension": "technical", "tips": ["Review core concepts."]}]),
    )
    db.session.add(report)
    db.session.commit()

    return interview.id


def test_generate_pdf_report(app, db, tmp_path):
    with app.app_context():
        interview_id = _setup_completed_interview(db)

        from APP.services.report_service import generate_pdf_report
        output_dir = str(tmp_path)
        pdf_path = generate_pdf_report(interview_id, output_dir=output_dir)

        assert os.path.exists(pdf_path)
        assert os.path.getsize(pdf_path) > 0

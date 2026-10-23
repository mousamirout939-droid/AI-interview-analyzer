"""
test_database.py
===================
Verifies ORM models can be created and related correctly.
"""

from APP.database import User, Interview, Analysis


def test_user_password_hashing(app, db):
    with app.app_context():
        user = User(full_name="Test User", email="hash@example.com", role="candidate")
        user.set_password("Secret123")
        db.session.add(user)
        db.session.commit()

        assert user.check_password("Secret123") is True
        assert user.check_password("wrong") is False


def test_interview_relationship(app, db):
    with app.app_context():
        user = User(full_name="Owner", email="owner@example.com", role="candidate")
        user.set_password("Secret123")
        db.session.add(user)
        db.session.commit()

        interview = Interview(
            user_id=user.id, title="Test Interview",
            original_filename="test.mp4", stored_filename="stored_test.mp4",
            file_type="video",
        )
        db.session.add(interview)
        db.session.commit()

        assert interview.id is not None
        assert user.interviews.count() == 1


def test_analysis_dimension_scores(app, db):
    with app.app_context():
        user = User(full_name="Scorer", email="scorer@example.com", role="candidate")
        user.set_password("Secret123")
        db.session.add(user)
        db.session.commit()

        interview = Interview(
            user_id=user.id, title="Scored Interview",
            original_filename="a.mp4", stored_filename="b.mp4", file_type="video",
        )
        db.session.add(interview)
        db.session.commit()

        analysis = Analysis(
            interview_id=interview.id, fluency_score=80, confidence_score=75,
            grammar_score=90, vocabulary_score=70, technical_score=65,
            communication_score=85, overall_score=77.5, verdict="Strong",
        )
        db.session.add(analysis)
        db.session.commit()

        scores = analysis.dimension_scores()
        assert scores["fluency"] == 80
        assert len(scores) == 6

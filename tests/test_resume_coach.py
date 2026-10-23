import io
import zipfile

from reportlab.pdfgen import canvas

from APP.services.resume_coach_service import (
    ResumeAnalysisError,
    analyze_resume,
    extract_resume_text,
)
from werkzeug.datastructures import FileStorage


def test_resume_recommends_track_guides_and_questions():
    result = analyze_resume(
        "Backend developer with Python, SQL, APIs, and database experience.",
        "auto",
    )

    assert result["track_key"] == "backend"
    assert "Python" in result["present_skills"]
    assert "Java" in result["missing_skills"]
    assert {"name": "Java", "slug": "java"} in result["recommended_guides"]
    assert result["questions"]
    categories = {category["title"]: category["questions"] for category in result["question_categories"]}
    assert "Technical questions" in categories
    assert any("Python" in question for question in categories["Technical questions"])
    assert "Aptitude & problem-solving questions" in categories
    assert "Behavioral questions" in categories


def test_resume_without_detected_skills_still_gets_practice_questions():
    result = analyze_resume("A motivated candidate looking for a first software role.", "general")
    categories = {category["title"]: category["questions"] for category in result["question_categories"]}

    assert categories["Resume & project questions"]
    assert categories["Technical questions"] == list(result["questions"])


def test_resume_target_role_overrides_keyword_inference():
    result = analyze_resume("Machine learning projects in Python.", "frontend")

    assert result["track_key"] == "frontend"
    assert result["track"]["title"] == "Frontend Development"


def test_c_family_language_keywords_are_detected():
    result = analyze_resume("Built projects in C++, C# and C programming.", "general")

    assert {"C++", "C#", "C"}.issubset(result["detected_skills"])


def test_extract_text_resume():
    upload = FileStorage(
        stream=io.BytesIO(b"Software developer experienced with Python and SQL."),
        filename="resume.txt",
    )

    assert "Python" in extract_resume_text(upload)


def test_extract_docx_resume():
    content = io.BytesIO()
    with zipfile.ZipFile(content, "w") as document:
        document.writestr(
            "word/document.xml",
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            "<w:body><w:p><w:r><w:t>Software developer with Python and SQL experience.</w:t>"
            "</w:r></w:p></w:body></w:document>",
        )
    upload = FileStorage(stream=io.BytesIO(content.getvalue()), filename="resume.docx")

    assert "Python" in extract_resume_text(upload)


def test_extract_pdf_resume():
    content = io.BytesIO()
    document = canvas.Canvas(content)
    document.drawString(72, 720, "Software developer with Python and SQL experience.")
    document.save()
    upload = FileStorage(stream=io.BytesIO(content.getvalue()), filename="resume.pdf")

    assert "Python" in extract_resume_text(upload)


def test_reject_unsupported_resume_format():
    upload = FileStorage(stream=io.BytesIO(b"resume"), filename="resume.rtf")

    try:
        extract_resume_text(upload)
    except ResumeAnalysisError as exc:
        assert "PDF, DOCX, or TXT" in str(exc)
    else:
        raise AssertionError("Unsupported file type should be rejected")


def test_resume_roadmap_requires_login(client):
    response = client.get("/resume/")

    assert response.status_code == 302
    assert "/auth/login" in response.location


def test_resume_roadmap_renders_result_without_storing_file(client):
    client.post(
        "/auth/register",
        data={
            "full_name": "Roadmap User",
            "email": "roadmap@example.com",
            "password": "Password1",
            "confirm_password": "Password1",
        },
        follow_redirects=True,
    )
    response = client.post(
        "/resume/",
        data={
            "target_role": "backend",
            "resume_file": (io.BytesIO(b"Backend engineer with Python and SQL experience."), "resume.txt"),
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"Your study roadmap" in response.data
    assert b"What questions could you be asked?" in response.data
    assert b"Technical questions" in response.data
    assert b"Python" in response.data
    assert b"Aptitude &amp; problem-solving questions" in response.data
    assert b"Open guide" in response.data

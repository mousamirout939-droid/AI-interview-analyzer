"""Extract resume text and create transparent, skill-based study suggestions."""

import io
import re
import zipfile
from xml.etree import ElementTree

from pypdf import PdfReader
from pypdf.errors import PdfReadError, PdfStreamError
from werkzeug.datastructures import FileStorage

from APP.services.learning_content import LEARNING_LANGUAGES

MAX_RESUME_BYTES = 5 * 1024 * 1024
MAX_RESUME_PAGES = 30
MAX_RESUME_TEXT_LENGTH = 200_000
MAX_DOCX_XML_BYTES = 10 * 1024 * 1024

_LEARNING_SLUGS = {language["slug"] for language in LEARNING_LANGUAGES}

_SKILLS = [
    ("Python", "python", (r"\bpython\b",)),
    ("JavaScript", "javascript", (r"\bjavascript\b", r"\bjs\b")),
    ("TypeScript", "typescript", (r"\btypescript\b", r"\bts\b")),
    ("HTML & CSS", "html-css", (r"\bhtml\b", r"\bcss\b")),
    ("Java", "java", (r"\bjava\b",)),
    ("C++", "cpp", (r"(?<!\w)c\+\+(?!\w)", r"\bcpp\b")),
    ("C#", "csharp", (r"(?<!\w)c#(?!\w)", r"\bcsharp\b")),
    ("C", "c", (r"\bc language\b", r"\bc programming\b", r"\bprogramming in c\b")),
    ("SQL", "sql", (r"\bsql\b",)),
    ("PHP", "php", (r"\bphp\b",)),
    ("Rust", "rust", (r"\brust\b",)),
    ("React", None, (r"\breact(?:\.js)?\b",)),
    ("Node.js", None, (r"\bnode(?:\.js)?\b",)),
    ("Django", None, (r"\bdjango\b",)),
    ("Flask", None, (r"\bflask\b",)),
    ("REST APIs", None, (r"\brest(?:ful)?\s+apis?\b", r"\bapi development\b")),
    ("Git", None, (r"\bgit(?:hub|lab)?\b",)),
    ("Docker", None, (r"\bdocker\b",)),
    ("Machine Learning", None, (r"\bmachine learning\b", r"\bdeep learning\b")),
    ("Data Structures", None, (r"\bdata structures?\b", r"\balgorithms?\b")),
    ("Cloud", None, (r"\baws\b", r"\bazure\b", r"\bgcp\b", r"\bcloud\b")),
]

_SKILL_QUESTIONS = {
    "Python": "What is the difference between a list and a tuple in Python, and when would you choose each?",
    "JavaScript": "How does asynchronous JavaScript work, and when would you use a Promise or async/await?",
    "TypeScript": "How do TypeScript interfaces and types help prevent errors in a larger codebase?",
    "HTML & CSS": "How would you make a page responsive and accessible across screen sizes?",
    "Java": "How do interfaces and inheritance differ in Java, and when would you use each?",
    "C++": "How do references and pointers differ in C++, and how do you manage object lifetime?",
    "C#": "How do async and await work in C#, and how should exceptions be handled in asynchronous code?",
    "C": "How do pointers work in C, and what steps help prevent memory errors?",
    "SQL": "How would you use joins and indexes to retrieve related records efficiently?",
    "PHP": "How does a web request move through a PHP application, and where would you validate input?",
    "Rust": "How do ownership and borrowing help Rust manage memory safely?",
    "React": "How do props and state differ in React, and how do you decide where state belongs?",
    "Node.js": "How does Node.js handle concurrent I/O, and what work could block its event loop?",
    "Django": "How do Django views, models, and URL patterns work together to serve a request?",
    "Flask": "How would you structure a Flask application as it grows beyond a few routes?",
    "REST APIs": "How would you choose HTTP methods and status codes for a REST API endpoint?",
    "Git": "How do you resolve a Git merge conflict and verify the resulting changes?",
    "Docker": "What belongs in a Docker image, and how would you pass configuration to a running container?",
    "Machine Learning": "How would you detect overfitting and choose an appropriate evaluation metric?",
    "Data Structures": "How would you choose a data structure for fast lookups, and what is its time complexity?",
    "Cloud": "How would you make a cloud-hosted service resilient to a failing instance?",
}

_APTITUDE_QUESTIONS = (
    "Given a list of numbers, how would you find a repeated value, and what is the time and space cost?",
    "If an application becomes slow after data grows tenfold, how would you investigate the bottleneck?",
    "How would you break a large problem into smaller steps and test each step?",
)

_BEHAVIORAL_QUESTIONS = (
    "Tell me about a time you had to learn a new tool or skill quickly. What was your approach?",
    "Describe a disagreement on a project and how you worked toward a resolution.",
    "Tell me about a mistake or setback and what you changed afterward.",
)

_TRACKS = {
    "backend": {
        "title": "Backend Development",
        "description": "Build server-side services, APIs, and data-backed applications.",
        "keywords": ("backend", "back-end", "server", "api", "microservice", "database"),
        "skills": ("Python", "Java", "SQL", "REST APIs", "Git", "Docker"),
        "questions": (
            "How would you design a REST API for a resource that needs filtering and pagination?",
            "Describe a database query or schema you improved and how you measured the result.",
            "How do you handle errors and retries when one service depends on another?",
        ),
    },
    "frontend": {
        "title": "Frontend Development",
        "description": "Create accessible, responsive interfaces that work well across devices.",
        "keywords": ("frontend", "front-end", "web interface", "user interface", "react", "css"),
        "skills": ("JavaScript", "TypeScript", "HTML & CSS", "React", "Git"),
        "questions": (
            "How do you make a web interface accessible to keyboard and screen-reader users?",
            "When would you choose local component state versus shared application state?",
            "How would you investigate a page that renders slowly on mobile?",
        ),
    },
    "full-stack": {
        "title": "Full-Stack Development",
        "description": "Connect polished web interfaces to reliable server-side systems.",
        "keywords": ("full stack", "full-stack", "frontend and backend", "end-to-end"),
        "skills": ("JavaScript", "TypeScript", "HTML & CSS", "Python", "SQL", "REST APIs"),
        "questions": (
            "Walk through how you would build and secure a feature from its UI to its database.",
            "How would you validate input consistently in both a browser and an API?",
            "Tell me about a bug that crossed the frontend/backend boundary and how you traced it.",
        ),
    },
    "data-ai": {
        "title": "Data & AI",
        "description": "Use programming, data, and evaluation to build useful analytical systems.",
        "keywords": ("data scientist", "data science", "machine learning", "artificial intelligence", "analytics"),
        "skills": ("Python", "SQL", "Machine Learning", "Data Structures"),
        "questions": (
            "How would you check whether a dataset is biased or has missing values?",
            "Explain how you would choose a metric for an imbalanced classification problem.",
            "Describe a model or analysis you built and how you evaluated whether it was useful.",
        ),
    },
    "general": {
        "title": "Software Development",
        "description": "Strengthen core programming skills and build a foundation for your next role.",
        "keywords": (),
        "skills": ("Python", "JavaScript", "SQL", "Git", "Data Structures"),
        "questions": (
            "Tell me about a project you are proud of and the decisions you made.",
            "How do you break down a problem when the requirements are unclear?",
            "Describe a time you received feedback and how you used it.",
        ),
    },
}


class ResumeAnalysisError(ValueError):
    """A resume could not be safely read or did not contain usable text."""


def extract_resume_text(upload: FileStorage | None) -> str:
    if upload is None or not upload.filename:
        raise ResumeAnalysisError("Choose a resume file to upload.")

    extension = upload.filename.rsplit(".", 1)[-1].lower() if "." in upload.filename else ""
    if extension not in {"pdf", "docx", "txt"}:
        raise ResumeAnalysisError("Use a PDF, DOCX, or TXT resume.")

    content = upload.stream.read(MAX_RESUME_BYTES + 1)
    if len(content) > MAX_RESUME_BYTES:
        raise ResumeAnalysisError("Resume files must be 5 MB or smaller.")
    if not content:
        raise ResumeAnalysisError("The selected resume file is empty.")

    if extension == "txt":
        try:
            text = content.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise ResumeAnalysisError("The TXT resume must use UTF-8 text encoding.") from exc
    elif extension == "docx":
        text = _extract_docx_text(content)
    else:
        text = _extract_pdf_text(content)

    text = re.sub(r"\s+", " ", text).strip()
    if len(text) < 40:
        raise ResumeAnalysisError(
            "We couldn't find enough readable text. Try a text-based PDF or DOCX, or upload a TXT file."
        )
    return text[:MAX_RESUME_TEXT_LENGTH]


def _extract_pdf_text(content: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(content), strict=False)
        if reader.is_encrypted:
            raise ResumeAnalysisError("This PDF is password-protected. Upload an unlocked copy.")
        if len(reader.pages) > MAX_RESUME_PAGES:
            raise ResumeAnalysisError(f"PDF resumes must have {MAX_RESUME_PAGES} pages or fewer.")
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except ResumeAnalysisError:
        raise
    except (OSError, ValueError, KeyError, PdfReadError, PdfStreamError, EOFError) as exc:
        raise ResumeAnalysisError("We couldn't read this PDF. Try exporting it again or use DOCX/TXT.") from exc


def _extract_docx_text(content: bytes) -> str:
    try:
        with zipfile.ZipFile(io.BytesIO(content)) as document:
            info = document.getinfo("word/document.xml")
            if info.file_size > MAX_DOCX_XML_BYTES:
                raise ResumeAnalysisError("This DOCX contains too much document data to process.")
            root = ElementTree.fromstring(document.read(info))
    except ResumeAnalysisError:
        raise
    except (zipfile.BadZipFile, KeyError, ElementTree.ParseError, OSError) as exc:
        raise ResumeAnalysisError("We couldn't read this DOCX. Try exporting it again or use PDF/TXT.") from exc

    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    return "\n".join(
        "".join(node.text or "" for node in paragraph.iter(f"{namespace}t"))
        for paragraph in root.iter(f"{namespace}p")
    )


def analyze_resume(resume_text: str, target_role: str = "auto") -> dict:
    normalized = resume_text.casefold()
    detected = {
        name
        for name, _slug, patterns in _SKILLS
        if any(re.search(pattern, normalized) for pattern in patterns)
    }

    track_key = target_role if target_role in _TRACKS and target_role != "auto" else _infer_track(normalized)
    track = _TRACKS[track_key]
    missing_skills = [skill for skill in track["skills"] if skill not in detected]
    recommended_guides = []
    for skill in missing_skills:
        slug = next((entry[1] for entry in _SKILLS if entry[0] == skill), None)
        if slug in _LEARNING_SLUGS:
            recommended_guides.append({"name": skill, "slug": slug})

    present_skills = [skill for skill in track["skills"] if skill in detected]
    technical_skills = [name for name, _slug, _patterns in _SKILLS if name in detected]
    technical_questions = [
        _SKILL_QUESTIONS[skill]
        for skill in technical_skills
        if skill in _SKILL_QUESTIONS
    ][:6]
    if not technical_questions:
        technical_questions = list(track["questions"])

    resume_questions = [
        f"You list {skill} on your resume. Describe a project where you used it and your specific contribution."
        for skill in technical_skills[:3]
    ]
    if not resume_questions:
        resume_questions.append(
            "Walk me through a project on your resume: what problem did it solve, and what part did you own?"
        )
    resume_questions.append(
        "What result or impact from your work are you most proud of, and how did you measure it?"
    )
    question_categories = [
        {"title": "Resume & project questions", "questions": resume_questions},
        {"title": "Technical questions", "questions": technical_questions},
        {"title": "Aptitude & problem-solving questions", "questions": list(_APTITUDE_QUESTIONS)},
        {"title": "Behavioral questions", "questions": list(_BEHAVIORAL_QUESTIONS)},
    ]
    roadmap = [
        {
            "title": "Build on your current strengths",
            "description": (
                f"Your resume mentions {', '.join(present_skills)}."
                if present_skills
                else "Start with programming fundamentals and version control."
            ),
        },
        {
            "title": "Focus on these next skills",
            "description": (
                ", ".join(missing_skills[:4]) if missing_skills
                else "Go deeper with projects and system design for your target role."
            ),
        },
        {
            "title": "Practise explaining your work",
            "description": "Use the role-specific questions below, then record an answer for feedback.",
        },
    ]

    return {
        "track": track,
        "track_key": track_key,
        "detected_skills": sorted(detected),
        "present_skills": present_skills,
        "missing_skills": missing_skills,
        "recommended_guides": recommended_guides,
        "roadmap": roadmap,
        "questions": track["questions"],
        "question_categories": question_categories,
    }


def _infer_track(resume_text: str) -> str:
    scores = {
        key: sum(bool(re.search(rf"\b{re.escape(keyword)}\b", resume_text)) for keyword in track["keywords"])
        for key, track in _TRACKS.items()
        if key != "general"
    }
    best_track = max(scores, key=scores.get)
    return best_track if scores[best_track] else "general"

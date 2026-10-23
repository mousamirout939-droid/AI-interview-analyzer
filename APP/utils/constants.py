"""
constants.py
==============
Shared application-wide constants: status enums, role names, upload
limits, and dimension labels used across controllers/templates.
"""

INTERVIEW_STATUS_UPLOADED = "uploaded"
INTERVIEW_STATUS_PROCESSING = "processing"
INTERVIEW_STATUS_COMPLETED = "completed"
INTERVIEW_STATUS_FAILED = "failed"

INTERVIEW_STATUSES = [
    INTERVIEW_STATUS_UPLOADED,
    INTERVIEW_STATUS_PROCESSING,
    INTERVIEW_STATUS_COMPLETED,
    INTERVIEW_STATUS_FAILED,
]

ROLE_CANDIDATE = "candidate"
ROLE_ADMIN = "admin"

SCORE_DIMENSIONS = ["fluency", "confidence", "grammar", "vocabulary", "technical", "communication"]

DIMENSION_DISPLAY_NAMES = {
    "fluency": "Fluency",
    "confidence": "Confidence",
    "grammar": "Grammar",
    "vocabulary": "Vocabulary",
    "technical": "Technical Depth",
    "communication": "Communication",
}

FLASH_SUCCESS = "success"
FLASH_ERROR = "error"
FLASH_INFO = "info"
FLASH_WARNING = "warning"

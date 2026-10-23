"""
notification_service.py
==========================
Lightweight in-app notification/flash-message helper. Structured so it
can later be extended to send real email notifications (e.g. "your
analysis is ready") without changing call sites in controllers.
"""

import logging
from flask import flash

logger = logging.getLogger("ai_interview_analyzer.notification_service")


def notify_user(message: str, category: str = "info") -> None:
    """Push a flash message to the current request/session."""
    flash(message, category)


def notify_analysis_complete(user_email: str, interview_title: str) -> None:
    """
    Placeholder hook for a future email/webhook integration. Currently just
    logs the event; wire up an email backend (Flask-Mail, SES, etc.) here
    for production notification delivery.
    """
    logger.info("Analysis complete notification (stub): %s -> '%s'", user_email, interview_title)

"""
logger.py
===========
Configures application-wide logging: console output plus a rotating file
handler under /logs so production deployments retain history without
unbounded log growth.
"""

import os
import logging
from logging.handlers import RotatingFileHandler

_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def configure_logging(app):
    """Attach console + rotating file handlers to the Flask app logger and root logger."""
    log_dir = os.path.join(_PROJECT_ROOT, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "app.log")

    formatter = logging.Formatter(_LOG_FORMAT)

    file_handler = RotatingFileHandler(log_path, maxBytes=2_000_000, backupCount=5)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG if app.debug else logging.INFO)

    root_logger = logging.getLogger("ai_interview_analyzer")
    root_logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
    root_logger.handlers.clear()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    root_logger.propagate = False

    app.logger.handlers = root_logger.handlers
    app.logger.setLevel(root_logger.level)

    return root_logger

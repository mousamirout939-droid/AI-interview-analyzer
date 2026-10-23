"""
gunicorn.conf.py
===================
Production WSGI server configuration for Gunicorn.

Usage:
    gunicorn -c deployment/gunicorn.conf.py "app:app"
"""

import multiprocessing
import os

bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"
workers = int(os.environ.get("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "sync"
timeout = int(os.environ.get("GUNICORN_TIMEOUT", 120))  # AI pipeline processing can take a while
graceful_timeout = 30
keepalive = 5

accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("LOG_LEVEL", "info")

preload_app = True

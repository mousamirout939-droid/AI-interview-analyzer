"""
response.py
=============
Standardized JSON API response builders used by AJAX-facing routes
(upload progress, analysis polling) so the frontend gets a consistent
envelope shape.
"""

from flask import jsonify


def success_response(data=None, message: str = "OK", status_code: int = 200):
    payload = {"success": True, "message": message, "data": data if data is not None else {}}
    return jsonify(payload), status_code


def error_response(message: str = "An error occurred", status_code: int = 400, errors=None):
    payload = {"success": False, "message": message, "errors": errors or []}
    return jsonify(payload), status_code

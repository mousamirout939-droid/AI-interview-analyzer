"""
error_handler.py (middleware)
================================
Registers global Flask error handlers (404, 403, 413, 500) that render
themed HTML error pages for browser requests and JSON envelopes for API
requests.
"""

import logging
from flask import render_template, request, jsonify

logger = logging.getLogger("ai_interview_analyzer.error_handler")


def _wants_json() -> bool:
    return request.path.startswith("/api/") or request.accept_mimetypes.best == "application/json"


def register_error_handlers(app):

    @app.errorhandler(403)
    def forbidden(error):
        if _wants_json():
            return jsonify({"success": False, "message": "Forbidden"}), 403
        return render_template("error.html", code=403, message="You don't have permission to access this page."), 403

    @app.errorhandler(404)
    def not_found(error):
        if _wants_json():
            return jsonify({"success": False, "message": "Not found"}), 404
        return render_template("error.html", code=404, message="The page you're looking for doesn't exist."), 404

    @app.errorhandler(413)
    def request_entity_too_large(error):
        if _wants_json():
            return jsonify({"success": False, "message": "File too large"}), 413
        return render_template("error.html", code=413, message="The uploaded file is too large."), 413

    @app.errorhandler(500)
    def internal_error(error):
        logger.exception("Internal server error: %s", error)
        if _wants_json():
            return jsonify({"success": False, "message": "Internal server error"}), 500
        return render_template("error.html", code=500, message="Something went wrong on our end. Please try again."), 500

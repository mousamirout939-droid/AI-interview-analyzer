"""
APP.routes
============
Aggregates all blueprints for single-call registration from the app
factory (APP/__init__.py).
"""

from APP.routes.auth_routes import auth_bp
from APP.routes.upload_routes import upload_bp
from APP.routes.dashboard_routes import dashboard_bp
from APP.routes.analysis_routes import analysis_bp
from APP.routes.report_routes import report_bp
from APP.routes.ranking_routes import ranking_bp
from APP.routes.history_routes import history_bp
from APP.routes.profile_routes import profile_bp
from APP.routes.learning_routes import learning_bp
from APP.routes.resume_routes import resume_bp

ALL_BLUEPRINTS = [
    auth_bp, upload_bp, dashboard_bp, analysis_bp,
    report_bp, ranking_bp, history_bp, profile_bp, learning_bp, resume_bp,
]

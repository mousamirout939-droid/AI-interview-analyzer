"""
APP/__init__.py
=================
Application factory for the AI Interview Analyzer. Wires together
configuration, the database, Flask-Login, blueprints, error handlers, and
template context processors (including the lavender/pink/green theme).
"""

import os
import logging

from flask import Flask
from flask_login import LoginManager

from config import get_config
from APP.database import db, User
from APP.routes import ALL_BLUEPRINTS
from APP.middleware.error_handler import register_error_handlers
from APP.utils.logger import configure_logging

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"


def create_app(config_object=None):
    app = Flask(__name__, static_folder="../static", template_folder="../templates")

    app.config.from_object(config_object or get_config())
    (config_object or get_config()).init_app(app)

    configure_logging(app)
    logger = logging.getLogger("ai_interview_analyzer.app")

    db.init_app(app)
    login_manager.init_app(app)

    for blueprint in ALL_BLUEPRINTS:
        app.register_blueprint(blueprint)

    register_error_handlers(app)
    _register_root_routes(app)
    _register_context_processors(app)

    with app.app_context():
        db.create_all()

    logger.info("AI Interview Analyzer application initialized (env=%s)", app.config.get("ENV", "unknown"))
    return app


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def _register_root_routes(app):
    from flask import render_template, redirect, url_for
    from flask_login import current_user

    @app.route("/")
    def landing():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard.index"))
        return render_template("index.html")

    @app.route("/health")
    def health():
        from evaluation.performance import get_performance_snapshot
        return get_performance_snapshot()


def _register_context_processors(app):
    @app.context_processor
    def inject_theme():
        return {"theme": app.config.get("THEME", {})}

    @app.context_processor
    def inject_helpers():
        from APP.utils.helpers import format_datetime, score_badge_class, truncate_text, seconds_to_mmss
        return {
            "format_datetime": format_datetime,
            "score_badge_class": score_badge_class,
            "truncate_text": truncate_text,
            "seconds_to_mmss": seconds_to_mmss,
        }

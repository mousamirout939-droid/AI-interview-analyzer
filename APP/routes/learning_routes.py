"""Browsable programming-language learning pages."""

from flask import Blueprint, abort, render_template

from APP.services.learning_content import LEARNING_LANGUAGES

learning_bp = Blueprint("learning", __name__, url_prefix="/learning")


@learning_bp.route("/")
def index():
    return render_template("learning.html", languages=LEARNING_LANGUAGES)


@learning_bp.route("/<slug>")
def language(slug):
    selected = next((item for item in LEARNING_LANGUAGES if item["slug"] == slug), None)
    if selected is None:
        abort(404)
    return render_template("learning_language.html", language=selected)

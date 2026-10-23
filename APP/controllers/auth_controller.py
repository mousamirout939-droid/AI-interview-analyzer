"""
auth_controller.py
=====================
Handles registration, login, logout request logic. Contains the
form-handling logic invoked by APP.routes.auth_routes; kept separate from
routing so it can be reused/tested independently of Flask's request
context wiring where practical.
"""

import logging
from flask import request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required, current_user

from APP.services.authentication_service import register_user, authenticate_user, AuthError
from flask import current_app

logger = logging.getLogger("ai_interview_analyzer.auth_controller")


def handle_register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        try:
            user = register_user(
                full_name=request.form.get("full_name", ""),
                email=request.form.get("email", ""),
                password=request.form.get("password", ""),
                confirm_password=request.form.get("confirm_password", ""),
                min_password_length=current_app.config.get("PASSWORD_MIN_LENGTH", 8),
            )
            login_user(user)
            flash("Welcome! Your account has been created.", "success")
            return redirect(url_for("dashboard.index"))
        except AuthError as exc:
            flash(str(exc), "error")
        except Exception:
            logger.exception("Unexpected error during registration")
            flash("Something went wrong creating your account. Please try again.", "error")

    return render_template("register.html")


def handle_login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        try:
            user = authenticate_user(request.form.get("email", ""), request.form.get("password", ""))
            login_user(user, remember=bool(request.form.get("remember")))
            flash(f"Welcome back, {user.full_name.split(' ')[0]}!", "success")
            next_url = request.args.get("next") or url_for("dashboard.index")
            return redirect(next_url)
        except AuthError as exc:
            flash(str(exc), "error")

    return render_template("login.html")


@login_required
def handle_logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))

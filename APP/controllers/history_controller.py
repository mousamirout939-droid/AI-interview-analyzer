"""
history_controller.py
========================
Renders the current user's interview history list (or all interviews, for
admins), with basic pagination.
"""

import logging
from flask import render_template, request, current_app
from flask_login import login_required, current_user

from APP.database import Interview

logger = logging.getLogger("ai_interview_analyzer.history_controller")


@login_required
def view_history():
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config.get("ITEMS_PER_PAGE", 10)

    query = Interview.query.order_by(Interview.created_at.desc())
    if not current_user.is_admin:
        query = query.filter_by(user_id=current_user.id)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template("history.html", interviews=pagination.items, pagination=pagination)

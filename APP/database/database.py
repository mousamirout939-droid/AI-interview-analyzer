"""
database.py
=============
Central SQLAlchemy extension instance shared by every model module. Kept
separate from app.py to avoid circular imports (models import `db` from
here; app.py imports `db` from here too and calls db.init_app(app)).
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

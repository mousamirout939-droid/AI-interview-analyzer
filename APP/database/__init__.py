"""
APP.database
=============
Exposes the shared `db` SQLAlchemy instance and all ORM models for
convenient single-point imports, e.g. `from APP.database import db, User`.
"""

from APP.database.database import db
from APP.database.user_model import User
from APP.database.interview_model import Interview
from APP.database.transcript_model import Transcript
from APP.database.analysis_model import Analysis
from APP.database.report_model import Report
from APP.database.ranking_model import Ranking

__all__ = ["db", "User", "Interview", "Transcript", "Analysis", "Report", "Ranking"]

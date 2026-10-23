"""
conftest.py
=============
Shared pytest fixtures: a Flask app configured with TestingConfig (an
in-memory SQLite database) and a test client for making requests.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# The web application and its extensions are optional for some unit tests.
# If the Flask app cannot be imported (missing optional test deps), don't
# register the Flask fixtures so lightweight tests can still run.
_app_available = True
try:
    from APP import create_app
    from APP.database import db as _db
    from config import TestingConfig
except Exception:
    _app_available = False


if _app_available:
    @pytest.fixture()
    def app():
        application = create_app(TestingConfig)
        yield application


    @pytest.fixture()
    def client(app):
        return app.test_client()


    @pytest.fixture()
    def db(app):
        with app.app_context():
            yield _db

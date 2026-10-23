"""
app.py
========
Application entry point. Run directly for local development:

    python app.py

For production, use gunicorn instead:

    gunicorn -c deployment/gunicorn.conf.py "app:app"
"""

import os
from APP import create_app

app = create_app()

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    debug = app.config.get("DEBUG", False)
    app.run(host=host, port=port, debug=debug)

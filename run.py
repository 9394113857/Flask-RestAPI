import os

from dotenv import load_dotenv

from app import create_app


# ============================================================
# Load environment variables
# ============================================================
# Local development:
#   Loads values from the .env file.
#
# Render:
#   Render provides environment variables directly.
# ============================================================

load_dotenv()


# ============================================================
# Create Flask application using the application factory
# ============================================================
# Gunicorn on Render imports this object using:
#
# gunicorn --bind 0.0.0.0:$PORT run:app
#
# Therefore:
#   run = Python module
#   app = Flask application object
# ============================================================

app = create_app()


# ============================================================
# Local development server
# ============================================================
# This block runs only when using:
#
# python run.py
#
# Gunicorn on Render imports "app" directly and does not
# execute this block.
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Port configuration
    # --------------------------------------------------------
    # Local:
    #   PORT=5000
    #
    # Render:
    #   Render provides the PORT environment variable.
    #
    # Default to 5000 for local development.
    # --------------------------------------------------------

    port = int(
        os.getenv(
            "PORT",
            "5000",
        )
    )

    # --------------------------------------------------------
    # Flask debug configuration
    # --------------------------------------------------------
    # Local:
    #   FLASK_DEBUG=true
    #
    # Render:
    #   FLASK_DEBUG=false
    # --------------------------------------------------------

    debug = (
        os.getenv(
            "FLASK_DEBUG",
            "true",
        ).lower()
        == "true"
    )

    # --------------------------------------------------------
    # Start Flask development server
    # --------------------------------------------------------

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug,
    )
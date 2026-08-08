import os

from dotenv import load_dotenv

from app import create_app


# Load environment variables from .env
load_dotenv()


# Create Flask application using the application factory
app = create_app()


if __name__ == "__main__":
    # Use PORT from environment variables.
    # Default to 5000 for local development.
    port = int(os.getenv("PORT", "5000"))

    # Enable/disable Flask debug mode.
    debug = os.getenv(
        "FLASK_DEBUG",
        "true",
    ).lower() == "true"

    # Start Flask development server.
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug,
    )
import os


# Project root directory
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)


class Config:
    # Database configuration
    #
    # Local development:
    # Uses SQLite database at:
    # instance/mobiles.db
    #
    # Production:
    # Set DATABASE_URL to the Supabase PostgreSQL
    # connection string.

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(
            BASE_DIR,
            "instance",
            "mobiles.db"
        )
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask JSON configuration
    JSON_SORT_KEYS = False

    # CORS configuration
    CORS_HEADERS = "Content-Type"
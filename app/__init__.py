from flask import Flask

from app.config import Config
from app.extensions import cors, db, migrate


def create_app(config_class=Config):
    """
    Application factory for the Flask REST API.
    """

    # --------------------------------------------------------
    # Create Flask application
    # --------------------------------------------------------

    app = Flask(__name__)

    # --------------------------------------------------------
    # Load application configuration
    # --------------------------------------------------------

    app.config.from_object(config_class)

    # --------------------------------------------------------
    # Initialize Flask extensions
    # --------------------------------------------------------

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # --------------------------------------------------------
    # Import models
    # --------------------------------------------------------
    # Required so Flask-Migrate / Alembic can detect the
    # SQLAlchemy models when generating migrations.
    # --------------------------------------------------------

    from app.models.mobile import Mobile

    # --------------------------------------------------------
    # Register API routes
    # --------------------------------------------------------

    from app.routes.mobile_routes import mobile_bp

    app.register_blueprint(mobile_bp)

    # --------------------------------------------------------
    # Health Check Endpoint
    # --------------------------------------------------------
    # Used by Render to verify that the application is alive.
    #
    # URL:
    #     GET /health
    # --------------------------------------------------------

    @app.route("/health", methods=["GET"])
    def health_check():
        return {
            "status": "ok",
            "service": "Flask REST API",
        }, 200

    # --------------------------------------------------------
    # Return configured Flask application
    # --------------------------------------------------------

    return app

from flask import Flask

from app.config import Config
from app.extensions import cors, db, migrate


def create_app(config_class=Config):
    app = Flask(__name__)

    # Load application configuration
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Import models so Flask-Migrate can detect them
    from app.models.mobile import Mobile

    # Register API routes
    from app.routes.mobile_routes import mobile_bp

    app.register_blueprint(mobile_bp)

    return app
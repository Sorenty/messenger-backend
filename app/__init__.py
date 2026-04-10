import uuid
from flask import Flask, g, request
from flask_session import Session
from redis import Redis

from config import Config
from .logging.logger import configure_logging
from .utils.db import db, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    configure_logging(app)

    if app.config.get("SESSION_TYPE") == "redis":
        app.config["SESSION_REDIS"] = Redis.from_url(app.config["SESSION_REDIS_URL"])

    Session(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import channels_bp
    app.register_blueprint(channels_bp, url_prefix="/api/channels")

    @app.before_request
    def set_request_id():
        g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

    @app.after_request
    def add_request_id_header(response):
        response.headers["X-Request-ID"] = g.request_id
        return response

    @app.route("/")
    def index():
        app.logger.info("root_hit", extra={"path": "/"})
        return {
            "status": "Messenger backend is running",
            "version": app.config.get("APP_VERSION", "dev"),
        }

    @app.route("/health")
    def health():
        app.logger.info("healthcheck")
        return {
            "status": "ok",
            "service": app.config.get("SERVICE_NAME", "messenger-backend"),
            "version": app.config.get("APP_VERSION", "dev"),
        }

    with app.app_context():
        app.logger.info("service_started", extra={"version": app.config.get("APP_VERSION", "dev")})

    return app
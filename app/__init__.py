from flask import Flask
from config import Config
from .utils.db import db, migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)

    # регистрируем блюпринты
    from .routes import channels_bp
    app.register_blueprint(channels_bp, url_prefix="/api/channels")

    # добавляем root route прямо сюда
    @app.route("/")
    def index():
        return {"status": "Messenger backend is running 🚀"}

    return app
from flask import Flask
from datetime import datetime
from core.config import Config
from core.database import StorageManager
from core.theme_loader import compile_themes
from auth.routes import bp as auth_bp
from api.analytics import bp as analytics_bp
from api.mobile import bp as mobile_bp
import routes

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    cfg = app.config
    compile_themes(cfg.get("THEME_DIR", "themes"),
                    cfg.get("STATIC_THEME_DIR", "static/themes"))

    # storage
    app.storage = StorageManager(app.config["DATABASE_PATH"])
    app.storage.init_lab_schemas()

    # blueprints
    app.register_blueprint(routes.bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(mobile_bp)

    @app.context_processor
    def inject_now():
        return {"now": datetime.utcnow()}

    return app
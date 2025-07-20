from flask import Flask
from datetime import datetime
from core.config import Config
from core.database import StorageManager
from core.theme_loader import compile_themes
from auth.routes import bp as auth_bp
from api.analytics import bp as analytics_bp
from api.mobile import bp as mobile_bp
from roles.user.blueprint import bp as user_bp
from roles.technician.blueprint import bp as tech_bp
from roles.admin.blueprint import bp as admin_bp
from api.qr import bp as qr_bp
import routes

app.register_blueprint(user_bp)
app.register_blueprint(tech_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(qr_bp)

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    config = Config()
    compile_themes(config.THEME_DIR, config.STATIC_THEME_DIR)

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
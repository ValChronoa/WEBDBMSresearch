from flask import Flask
from core.config import Config
from core.database import StorageManager
from core.theme_loader import compile_themes

# blueprints
from auth.routes import auth_bp
from main.routes import main_bp
from roles.user.blueprint import user_bp
from roles.technician.blueprint import tech_bp
from roles.admin.blueprint import admin_bp
from api.qr import qr_bp
from api.analytics import bp as analytics_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialise storage singletons
    app.storage     = StorageManager(app.config['DATABASE_PATH'])
    app.users_store = StorageManager(app.config['USERS_PATH'])

    # compile CSS themes once at startup
    compile_themes(app.config['THEME_DIR'], app.config['STATIC_THEME_DIR'])

    # register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp,   url_prefix='/auth')
    app.register_blueprint(user_bp,   url_prefix='/user')
    app.register_blueprint(tech_bp,   url_prefix='/tech')
    app.register_blueprint(admin_bp,  url_prefix='/admin')
    app.register_blueprint(qr_bp,     url_prefix='/api/qr')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')

    # context processor for timestamps
    @app.context_processor
    def inject_now():
        from datetime import datetime
        return {"now": datetime.utcnow()}

    return app
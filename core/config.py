import os
from pathlib import Path

class Config:
    SECRET_KEY           = os.getenv("SECRET_KEY") or "dev-secret-change-me"
    DATABASE_PATH        = os.getenv("DATABASE_PATH") or "database.json"
    USERS_PATH           = os.getenv("USERS_PATH") or "users.json"
    THEME_DIR            = os.getenv("THEME_DIR") or "static/themes"
    STATIC_THEME_DIR     = os.getenv("STATIC_THEME_DIR") or "static/css/themes"
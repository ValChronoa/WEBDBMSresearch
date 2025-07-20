from dataclasses import dataclass
import os

@dataclass  # <-- remove slots=True
class Config:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-key-change-me")
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "database.json")
    THEME_DIR: str = os.getenv("THEME_DIR", "themes")
    STATIC_THEME_DIR: str = os.getenv("STATIC_THEME_DIR", "static/themes")
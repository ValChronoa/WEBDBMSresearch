"""Global configuration singleton."""
from __future__ import annotations
import os
from dataclasses import dataclass

@dataclass(slots=True)
class Config:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-key-change-me")
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "database.json")
    THEME_DIR: str = os.getenv("THEME_DIR", "themes")
    STATIC_THEME_DIR: str = "static/themes"
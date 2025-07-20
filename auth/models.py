from __future__ import annotations
import uuid, jwt, os
from werkzeug.security import generate_password_hash, check_password_hash
from core.database import StorageManager
from datetime import datetime, timedelta

SECRET = os.getenv("JWT_SECRET", "dev-secret")

class User:
    ROLES = {"user", "technician", "admin"}

    def __init__(self, username: str, password: str, role: str = "user", lab: str | None = None):
        if role not in self.ROLES:
            raise ValueError("Invalid role")
        self.id = uuid.uuid4().hex[:8]
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.role = role
        self.lab = lab  # only for technician

    # --- CRUD helpers ---
    @classmethod
    def find(cls, username: str):
        db = StorageManager("users.json")
        users = db.list_items("users")
        for uid, data in users.items():
            if data["username"] == username:
                return uid, User(**data)
        return None, None

    @classmethod
    def find_by_id(cls, uid: str):
        db = StorageManager("users.json")
        data = db.list_items("users").get(uid)
        return User(**data) if data else None

    def save(self):
        db = StorageManager("users.json")
        db.add_item("users", self.__dict__)

    # --- JWT helpers ---
    @classmethod
    def decode_token(cls, token: str):
        try:
            payload = jwt.decode(token, SECRET, algorithms=["HS256"])
            return cls.find_by_id(payload["sub"])
        except jwt.ExpiredSignatureError:
            return None
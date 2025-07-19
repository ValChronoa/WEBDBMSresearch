from __future__ import annotations
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from core.database import StorageManager

class User:
    ROLES = {"admin", "teacher", "student"}

    def __init__(self, username: str, password: str, role: str = "student"):
        if role not in self.ROLES:
            raise ValueError("Invalid role")
        self.id = uuid.uuid4().hex[:8]
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.role = role

    @classmethod
    def find(cls, username: str):
        db = StorageManager("users.json")
        users = db.list_items("users")
        for uid, data in users.items():
            if data["username"] == username:
                return uid, data
        return None, None

    def save(self):
        db = StorageManager("users.json")
        db.add_item("users", self.__dict__)
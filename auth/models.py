from __future__ import annotations
import uuid, jwt, os
from werkzeug.security import generate_password_hash, check_password_hash
from core.database import StorageManager
from datetime import datetime, timedelta

SECRET = os.getenv("JWT_SECRET", "dev-secret")

class User:
    ROLES = {"user", "technician", "admin"}

    def __init__(
        self,
        username: str,
        password: str,
        role: str = "user",
        lab: str | None = None,
    ):
        if role not in self.ROLES:
            raise ValueError("Invalid role")
        self.id = uuid.uuid4().hex[:8]
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.role = role
        self.lab = lab

    # -------------------------
    # CRUD helpers
    # -------------------------
    @classmethod
    def find(cls, username: str, store: StorageManager):
        """
        Return (uid, User) for the given username.
        Uses the StorageManager provided by the caller.
        """
        users = store.list_items("users")
        for uid, data in users.items():
            if data.get("username") == username:
                # Build User without re-hashing password
                user = cls.__new__(cls)
                user.id = uid
                for k, v in data.items():
                    setattr(user, k, v)
                return uid, user
        return None, None

    @classmethod
    def find_by_id(cls, uid: str, store: StorageManager):
        data = store.list_items("users").get(uid)
        if not data:
            return None
        user = cls.__new__(cls)
        user.id = uid
        for k, v in data.items():
            setattr(user, k, v)
        return user

    def save(self, store: StorageManager):
        """Persist this user via the provided StorageManager."""
        store.add_item("users", self.__dict__)

    # -------------------------
    # JWT helpers
    # -------------------------
    @classmethod
    def decode_token(cls, token: str, store: StorageManager):
        try:
            payload = jwt.decode(token, SECRET, algorithms=["HS256"])
            return cls.find_by_id(payload["sub"], store=store)
        except jwt.ExpiredSignatureError:
            return None
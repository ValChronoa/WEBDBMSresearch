import json, os, uuid, threading
from typing import Any, Dict

class StorageManager:
    _lock = threading.RLock()

    def __init__(self, path: str):
        self._path = path
        self._data: Dict[str, Dict[str, Any]] = {}
        self._load()

    def init_lab_schemas(self):
        for lab in ("physics", "chemistry", "biology"):
            self._data.setdefault(lab, {})
        self._save()

    def add_item(self, lab: str, item: Dict[str, Any]) -> str:
        with self._lock:
            uid = uuid.uuid4().hex[:8]
            self._data.setdefault(lab, {})[uid] = item
            self._save()
            return uid

    def update_item(self, lab: str, uid: str, item: Dict[str, Any]) -> None:
        with self._lock:
            self._data[lab][uid].update(item)
            self._save()

    def delete_item(self, lab: str, uid: str) -> None:
        with self._lock:
            self._data[lab].pop(uid, None)
            self._save()

    def list_items(self, lab: str) -> Dict[str, Dict[str, Any]]:
        return self._data.get(lab, {}).copy()

    def _load(self):
        if os.path.exists(self._path):
            with open(self._path, encoding="utf-8") as fp:
                self._data = json.load(fp)

    def _save(self):
        with open(self._path, "w", encoding="utf-8") as fp:
            json.dump(self._data, fp, indent=2)
# core/database.py
import json
import os
import uuid
import threading
from pathlib import Path
from typing import Dict, Any, List

class StorageManager:
    """
    Thread-safe, atomic JSON store that also knows the canonical
    field lists for each lab.
    """

    _lock = threading.Lock()

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._ensure_file()

    # ------------------------------------------------------------------
    # Low-level file utilities
    # ------------------------------------------------------------------
    def _ensure_file(self) -> None:
        """Create parent dirs and an empty JSON dict if necessary."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("{}")

    def _read_atomic(self) -> Dict[str, Any]:
        """Read the entire file under lock."""
        with self._lock:
            with self.file_path.open("r", encoding="utf-8") as f:
                return json.load(f)

    def _write_atomic(self, data: Dict[str, Any]) -> None:
        """Write the entire file atomically under lock."""
        with self._lock:
            tmp = self.file_path.with_suffix(".tmp")
            with tmp.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, self.file_path)

    # ------------------------------------------------------------------
    # Public CRUD interface (unchanged signatures)
    # ------------------------------------------------------------------
    def init_lab_schemas(self) -> None:
        """Create keys for physics, chemistry, biology if missing."""
        data = self._read_atomic()
        for lab in ("physics", "chemistry", "biology"):
            data.setdefault(lab, {})
        self._write_atomic(data)

    def add_item(self, lab: str, item: Dict[str, Any]) -> str:
        data = self._read_atomic()
        uid = uuid.uuid4().hex[:8]
        data.setdefault(lab, {})[uid] = item
        self._write_atomic(data)
        return uid

    def update_item(self, lab: str, uid: str, item: Dict[str, Any]) -> None:
        data = self._read_atomic()
        if lab in data and uid in data[lab]:
            data[lab][uid].update(item)
            self._write_atomic(data)

    def delete_item(self, lab: str, uid: str) -> None:
        data = self._read_atomic()
        data.get(lab, {}).pop(uid, None)
        self._write_atomic(data)

    def list_items(self, lab: str) -> Dict[str, Dict[str, Any]]:
        """Return a *shallow* copy of the requested lab dict."""
        return self._read_atomic().get(lab, {}).copy()

    # ------------------------------------------------------------------
    # Schema helpers (from old project)
    # ------------------------------------------------------------------
    @staticmethod
    def get_lab_fields(lab_name: str) -> List[str]:
        fields = {
            "chemistry": [
                "name", "quantity", "supplier_name", "supplier_address",
                "supplier_phone", "cas_number", "signal_word", "hazards",
                "pictogram", "precautionary_statements", "supplemental_info",
                "distributor_name", "distributor_phone", "date_purchased",
                "date_opened", "expiration_date"
            ],
            "biology": [
                "name", "quantity", "storage_conditions", "biohazard_level",
                "supplier_name", "supplier_contact", "catalog_number",
                "expiration_date", "date_received", "date_opened",
                "last_used", "used_by", "disposal_method", "notes"
            ],
            "physics": [
                "name", "quantity", "manufacturer", "model_number",
                "serial_number", "location", "calibration_due",
                "last_calibration", "condition", "current_user",
                "usage_log", "notes"
            ]
        }
        return fields.get(lab_name, [])
"""Inventory analytics engine (JSON-native)."""
from __future__ import annotations
import datetime as dt
from typing import Dict, List, Any

class AnalyticsEngine:
    @staticmethod
    def aging_report(lab: str, data: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        today = dt.date.today()
        buckets = {"<30": 0, "30-60": 0, "60-90": 0, ">90": 0}
        for item in data.values():
            date_str = item.get("expiration_date") or item.get("calibration_due")
            if not date_str:
                continue
            try:
                delta = (today - dt.datetime.strptime(date_str, "%m-%d-%Y").date()).days
            except ValueError:
                continue
            key = "<30" if delta < 30 else "30-60" if delta < 60 else "60-90" if delta < 90 else ">90"
            buckets[key] += 1
        return [{"bucket": k, "count": v} for k, v in buckets.items()]

    @staticmethod
    def compliance_forecast(lab: str, data: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        today = dt.date.today()
        future = today + dt.timedelta(days=30)
        out = []
        for uid, item in data.items():
            date_str = item.get("expiration_date") or item.get("calibration_due")
            if not date_str:
                continue
            try:
                target = dt.datetime.strptime(date_str, "%m-%d-%Y").date()
            except ValueError:
                continue
            if today <= target <= future:
                out.append({"id": uid, "name": item["name"], "due": target.isoformat()})
        return sorted(out, key=lambda x: x["due"])

    @staticmethod
    def usage_pattern(lab: str, data: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        counter = {}
        for item in data.values():
            cond = item.get("condition", "Unknown")
            counter[cond] = counter.get(cond, 0) + 1
        return [{"condition": k, "count": v} for k, v in counter.items()]
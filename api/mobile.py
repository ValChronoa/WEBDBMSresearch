"""Mobile-only endpoints (offline sync & push)."""
from __future__ import annotations
from flask import Blueprint, request, jsonify, current_app

bp = Blueprint("mobile_api", __name__, url_prefix="/api/mobile")

@bp.route("/sync", methods=["POST"])
def sync():
    payload = request.get_json()
    lab = payload.pop("lab")
    uid = current_app.storage.add_item(lab, payload)
    return jsonify({"id": uid}), 201
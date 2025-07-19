"""Analytics REST endpoints."""
from __future__ import annotations
from flask import Blueprint, jsonify, current_app
from analytics.engine import AnalyticsEngine

bp = Blueprint("analytics_api", __name__, url_prefix="/api/analytics")

@bp.route("/<lab>/aging")
def aging(lab: str):
    data = current_app.storage.list_items(lab.lower())
    return jsonify(AnalyticsEngine.aging_report(lab, data))

@bp.route("/<lab>/forecast")
def forecast(lab: str):
    data = current_app.storage.list_items(lab.lower())
    return jsonify(AnalyticsEngine.compliance_forecast(lab, data))

@bp.route("/<lab>/usage")
def usage(lab: str):
    data = current_app.storage.list_items(lab.lower())
    return jsonify(AnalyticsEngine.usage_pattern(lab, data))
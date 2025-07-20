from flask import Blueprint, render_template, send_file, session, current_app
from core.database import StorageManager
import io, csv
from datetime import datetime

tech_bp = Blueprint("tech", __name__, url_prefix="/tech")

# ------------------------------------------------------------------
# Helper: StorageManager wired to live config
# ------------------------------------------------------------------
def _store() -> StorageManager:
    return StorageManager(current_app.config['DATABASE_PATH'])

# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------
@tech_bp.route("/")
def dashboard():
    lab = session.get("lab")
    if not lab:
        return "Access denied", 403
    items = [{"id": k, **v} for k, v in _store().list_items(lab).items()]
    return render_template("technician/lab.html", lab=lab, items=items)


@tech_bp.route("/export/<lab>")
def export_csv(lab):
    items = [{"id": k, **v} for k, v in _store().list_items(lab).items()]
    if not items:
        return "No data to export", 204

    # Use the canonical field list for this lab
    fields = _store().get_lab_fields(lab)
    if not fields:
        fields = ["id", "name", "quantity"]   # fallback

    si = io.StringIO()
    writer = csv.DictWriter(si, fieldnames=["id"] + fields)
    writer.writeheader()
    for row in items:
        writer.writerow({k: row.get(k, "") for k in ["id"] + fields})

    return send_file(
        io.BytesIO(si.getvalue().encode()),
        as_attachment=True,
        download_name=f"{lab}_{datetime.utcnow().strftime('%Y%m%d')}.csv",
        mimetype="text/csv"
    )


@tech_bp.route("/invoice/<lab>/<item_id>")
def invoice(lab, item_id):
    item = _store().list_items(lab).get(item_id)
    return render_template("technician/invoice.html", item=item, lab=lab)
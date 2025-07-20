from flask import Blueprint, render_template, request, send_file, session
from core.database import StorageManager
import io, csv, json

bp = Blueprint("tech", __name__, url_prefix="/tech")

@bp.route("/")
def dashboard():
    lab = session.get("lab")
    if not lab:
        return "Access denied", 403
    items = StorageManager("database.json").list_items(lab)
    return render_template("technician/lab.html", lab=lab, items=items)

@bp.route("/export/<lab>")
def export_csv(lab):
    items = StorageManager("database.json").list_items(lab)
    si = io.StringIO()
    writer = csv.DictWriter(si, fieldnames=["id", "name", "quantity", "condition"])
    writer.writeheader()
    for k, v in items.items():
        writer.writerow({"id": k, **v})
    return send_file(
        io.BytesIO(si.getvalue().encode()),
        as_attachment=True,
        download_name=f"{lab}.csv",
        mimetype="text/csv"
    )

@bp.route("/invoice/<lab>/<item_id>")
def invoice(lab, item_id):
    db = StorageManager("database.json")
    item = db.list_items(lab).get(item_id)
    return render_template("technician/invoice.html", item=item, lab=lab)
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, Response
import csv, json, io

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    stats = {lab: len(current_app.storage.list_items(lab)) for lab in ("physics", "chemistry", "biology")}
    return render_template("index.html", labs=("physics", "chemistry", "biology"), lab_stats=stats)

@bp.route("/lab/<lab_name>")
def lab_inventory(lab_name):
    lab = lab_name.lower()
    items_raw = current_app.storage.list_items(lab)
    items = [{"id": k, **v} for k, v in items_raw.items()]
    return render_template("lab.html", lab_name=lab, items=items)

@bp.route("/lab/<lab_name>/add", methods=("GET", "POST"))
def add_item(lab_name):
    lab = lab_name.lower()
    if request.method == "POST":
        current_app.storage.add_item(lab, dict(request.form))
        flash("Item added.", "success")
        return redirect(url_for("main.lab_inventory", lab_name=lab))
    fields = _fields_for(lab)
    return render_template("add_edit_item.html", lab_name=lab, fields=fields)

@bp.route("/lab/<lab_name>/edit/<item_id>", methods=("GET", "POST"))
def edit_item(lab_name, item_id):
    lab = lab_name.lower()
    if request.method == "POST":
        current_app.storage.update_item(lab, item_id, dict(request.form))
        flash("Updated.", "success")
        return redirect(url_for("main.lab_inventory", lab_name=lab))
    item = current_app.storage.list_items(lab)[item_id]
    fields = _fields_for(lab)
    return render_template("add_edit_item.html", lab_name=lab, fields=fields, item=item, item_id=item_id)

@bp.route("/lab/<lab_name>/delete/<item_id>", methods=("POST",))
def delete_item(lab_name, item_id):
    lab = lab_name.lower()
    current_app.storage.delete_item(lab, item_id)
    flash("Deleted.", "warning")
    return redirect(url_for("main.lab_inventory", lab_name=lab))

@bp.route("/lab/<lab_name>/export", methods=("GET", "POST"))
def export_lab(lab_name):
    lab = lab_name.lower()
    items = current_app.storage.list_items(lab)
    if request.method == "POST":
        fmt = request.form["format"]
        if fmt == "csv":
            return _export_csv(items, lab)
        return _export_json(items, lab)
    return render_template("export.html", lab_name=lab)

@bp.route("/lab/<lab_name>/analytics")
def analytics_page(lab_name):
    return render_template("analytics.html", lab=lab_name.lower())

def _fields_for(lab):
    common = ["name", "quantity", "location", "notes"]
    if lab == "physics":
        return common + ["manufacturer", "model_number", "serial_number", "calibration_due", "last_calibration", "condition", "current_user", "usage_log"]
    if lab == "chemistry":
        return common + ["manufacturer", "expiration_date", "supplier", "hazard_class"]
    return common + ["manufacturer", "storage_temp", "biohazard_level"]

def _export_csv(data, lab):
    if not data:
        return Response("No data", mimetype="text/plain")
    si = io.StringIO()
    keys = list(next(iter(data.values())).keys()) + ["id"]
    writer = csv.DictWriter(si, fieldnames=keys)
    writer.writeheader()
    for uid, v in data.items():
        writer.writerow({"id": uid, **v})
    return Response(si.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": f"attachment; filename={lab}.csv"})

def _export_json(data, lab):
    return Response(json.dumps(data, indent=2), mimetype="application/json",
                    headers={"Content-Disposition": f"attachment; filename={lab}.json"})
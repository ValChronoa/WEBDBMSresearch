from flask import Blueprint, render_template, send_file, request, session, redirect, url_for, flash, current_app
from core.decorators import role_required
from flask import current_app as app
from core.database import StorageManager
import io, csv
from datetime import datetime, timedelta
from core.decorators import role_required

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
@role_required("technician")
def dashboard():
    lab = session.get("lab")
    if not lab:
        return "Access denied", 403
    items = [{"id": k, **v} for k, v in _store().list_items(lab).items()]
    return render_template("technician/lab.html", lab=lab, items=items)

# ------------------------------------------------------------------
# Add Item Route
# ------------------------------------------------------------------
@tech_bp.route("/add/<lab>", methods=["GET", "POST"])
@role_required("technician")
def add_item(lab):
    if request.method == "POST":
        # Collect all fields from form
        fields = request.form.to_dict()
        # Remove empty fields
        fields = {k: v for k, v in fields.items() if v != ""}
        # Required fields
        name = fields.get("name")
        quantity = fields.get("quantity")
        if not name or not quantity:
            flash("Name and quantity are required.", "danger")
            return redirect(url_for("tech.add_item", lab=lab))
        # Convert quantity to int or float
        try:
            if "." in quantity:
                quantity = str(float(quantity))
            else:
                quantity = str(int(quantity))
        except Exception:
            flash("Invalid quantity.", "danger")
            return redirect(url_for("tech.add_item", lab=lab))
        fields["quantity"] = quantity
        # Generate a simple unique ID
        item_id = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        # Set default borrow fields as empty strings
        fields["borrowed_by"] = ""
        fields["borrowed_on"] = ""
        fields["returned_on"] = ""
        fields["return_notes"] = ""
        _store().update_item(lab, item_id, fields)
        flash(f"Item '{name}' added.", "success")
        return redirect(url_for("tech.dashboard"))
    # Get lab fields for dynamic form
    lab_fields = _store().get_lab_fields(lab)
    return render_template("technician/add_item.html", lab=lab, lab_fields=lab_fields)

# ------------------------------------------------------------------
# Edit Item Route
# ------------------------------------------------------------------
@tech_bp.route("/edit/<lab>/<item_id>", methods=["GET", "POST"])
@role_required("technician")
def edit_item(lab, item_id):
    item = _store().list_items(lab).get(item_id)
    if not item:
        flash("Item not found.", "danger")
        return redirect(url_for("tech.dashboard"))
    if request.method == "POST":
        fields = request.form.to_dict()
        fields = {k: v for k, v in fields.items() if v != ""}
        name = fields.get("name")
        quantity = fields.get("quantity")
        if not name or not quantity:
            flash("Name and quantity are required.", "danger")
            return redirect(url_for("tech.edit_item", lab=lab, item_id=item_id))
        try:
            if "." in quantity:
                quantity = str(float(quantity))
            else:
                quantity = str(int(quantity))
        except Exception:
            flash("Invalid quantity.", "danger")
            return redirect(url_for("tech.edit_item", lab=lab, item_id=item_id))
        fields["quantity"] = quantity
        # Preserve borrow/return fields as strings
        for k in ["borrowed_by", "borrowed_on", "returned_on", "return_notes"]:
            v = item.get(k)
            fields[k] = v if v is not None else ""
        _store().update_item(lab, item_id, fields)
        flash(f"Item '{name}' updated.", "success")
        return redirect(url_for("tech.dashboard"))
    lab_fields = _store().get_lab_fields(lab)
    return render_template("technician/edit_item.html", lab=lab, item=item, item_id=item_id, lab_fields=lab_fields)

@tech_bp.route("/export/<lab>")
@role_required("technician")
def export_csv(lab):
    items = [{"id": k, **v} for k, v in _store().list_items(lab).items()]
    if not items:
        return "No data to export", 204

    fields = _store().get_lab_fields(lab)
    if not fields:
        fields = ["id", "name", "quantity"]

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
@role_required("technician")
def invoice(lab, item_id):
    item = _store().list_items(lab).get(item_id)
    return render_template("technician/invoice.html", item=item, lab=lab)

@tech_bp.route("/log")
@role_required("technician")
def borrow_log():
    lab = session.get("lab")
    if not lab:
        return "Access denied", 403
    items = [{"id": k, **v} for k, v in _store().list_items(lab).items()]
    return render_template("technician/log.html", lab=lab, items=items)

# ------------------------------------------------------------------
# Borrow / Return / Receipt routes
# ------------------------------------------------------------------
@tech_bp.route("/borrow/<lab>/<item_id>", methods=["POST"])
@role_required("technician")
def mark_borrowed(lab, item_id):
    student = request.form["student"]
    borrow_quantity = request.form.get("borrow_quantity", "")
    # Store borrow_quantity as a string, can be mL, g, etc.
    _store().update_item(lab, item_id, {
        "borrowed_by": student,
        "borrowed_on": datetime.utcnow().isoformat(timespec="seconds"),
        "returned_on": "",
        "return_notes": "",
        "borrow_quantity": borrow_quantity
    })
    flash("Marked borrowed", "success")
    return redirect(url_for("tech.borrow_log"))

@tech_bp.route("/return/<lab>/<item_id>", methods=["POST"])
@role_required("technician")
def mark_returned(lab, item_id):
    notes = request.form["notes"]
    _store().update_item(lab, item_id, {
        "returned_on": datetime.utcnow().isoformat(timespec="seconds"),
        "return_notes": notes,
        "borrowed_by": None,      # Clear borrower
        "borrowed_on": None       # Clear borrowed date
    })
    flash("Marked returned", "success")
    return redirect(url_for("tech.borrow_log"))

@tech_bp.route("/receipt/<lab>/<item_id>")
@role_required("technician")
def receipt(lab, item_id):
    item = _store().list_items(lab).get(item_id)
    if not item or not item.get("borrowed_by"):
        return "No active loan", 404

    due = datetime.fromisoformat(item["borrowed_on"]) + timedelta(days=7)
    payload = {
        "lab": lab,
        "item_id": item_id,
        "name": item["name"],
        "borrowed_by": item["borrowed_by"],
        "borrowed_on": item["borrowed_on"],
        "return_due": due.isoformat(timespec="seconds")
    }
    return render_template("technician/receipt_qr.html", payload=payload)
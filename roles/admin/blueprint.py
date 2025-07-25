# roles/admin/blueprint.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from core.decorators import role_required
from core.database import StorageManager
from core.decorators import role_required
from auth.models import User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# ------------------------------------------------------------------
# Helper
# ------------------------------------------------------------------
def _store() -> StorageManager:
    return StorageManager(current_app.config['DATABASE_PATH'])

def _users_store() -> StorageManager:
    return StorageManager(current_app.config['USERS_PATH'])

# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------
@admin_bp.route("/")
@role_required("admin")
def dashboard():
    labs = ["physics", "chemistry", "biology"]
    stats = {lab: len(_store().list_items(lab)) for lab in labs}
    users = _users_store().list_items("users")
    return render_template("admin/dashboard.html", stats=stats, users=users)


@admin_bp.route("/lab/<lab_name>", methods=["GET", "POST"])
@role_required("admin")
def lab_view(lab_name):
    if request.method == "POST":
        item_id = request.form.get("item_id")
        action = request.form.get("action")
        if item_id and action:
            item = _store().list_items(lab_name).get(item_id)
            if item:
                if action == "set_available":
                    item["returned_on"] = ""
                    item["borrowed_by"] = ""
                    _store().update_item(lab_name, item_id, item)
                    flash("Item set to Available.", "success")
                elif action == "set_returned":
                    from datetime import datetime
                    item["returned_on"] = datetime.utcnow().isoformat(timespec="seconds")
                    _store().update_item(lab_name, item_id, item)
                    flash("Item set to Returned.", "success")
        return redirect(url_for("admin.lab_view", lab_name=lab_name))
    items = [{"id": k, **v} for k, v in _store().list_items(lab_name).items()]
    q = request.args.get("q", "").strip().lower()
    if q:
        def matches(item):
            return any(q in str(v).lower() for v in item.values())
        items = [item for item in items if matches(item)]
    return render_template("admin/lab.html", lab=lab_name, items=items)


@admin_bp.route("/user/add", methods=["GET", "POST"])
@role_required("admin")
def add_user():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        lab = request.form.get("lab") if role == "technician" else None

        uid, existing = User.find(username, store=_users_store())
        if existing:
            flash("Username already exists", "danger")
            return redirect(url_for("admin.add_user"))

        user = User(username, password, role, lab)
        user.save(store=_users_store())
        flash("User created", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/add_user.html")


@admin_bp.route("/user/delete/<uid>")
@role_required("admin")
def delete_user(uid):
    _users_store().delete_item("users", uid)
    flash("User removed", "success")
    return redirect(url_for("admin.dashboard"))
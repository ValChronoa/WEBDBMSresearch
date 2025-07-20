from flask import Blueprint, render_template, request
from core.database import StorageManager

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.route("/")
def dashboard():
    db = StorageManager("database.json")
    labs = ("physics", "chemistry", "biology")
    stats = {lab: len(db.list_items(lab)) for lab in labs}
    return render_template("admin/dashboard.html", labs=labs, stats=stats)

@bp.route("/lab/<lab_name>")
def lab_view(lab_name):
    items = StorageManager("database.json").list_items(lab_name)
    return render_template("admin/lab.html", lab_name=lab_name, items=items)
from flask import Blueprint, render_template, request, redirect, url_for, session
from auth.models import User

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/")
def dashboard():
    labs = ("physics", "chemistry", "biology")
    from core.database import StorageManager
    db = StorageManager("database.json")
    stats = {lab: len(db.list_items(lab)) for lab in labs}
    return render_template("user/index.html", labs=labs, stats=stats)

@bp.route("/lab/<lab_name>")
def lab_view(lab_name):
    db = StorageManager("database.json")
    items = [{"id": k, **v} for k, v in db.list_items(lab_name).items()]
    return render_template("user/lab.html", lab_name=lab_name, items=items)

@bp.route("/status/<lab_name>/<item_id>")
def status(lab_name, item_id):
    db = StorageManager("database.json")
    item = db.list_items(lab_name).get(item_id)
    return render_template("user/status.html", item=item)
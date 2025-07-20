# roles/user/blueprint.py
from flask import Blueprint, render_template, session, current_app
from core.database import StorageManager

user_bp = Blueprint('user', __name__, url_prefix='/user')

# -------------------------------------------------
# Helper: StorageManager wired to live config
# -------------------------------------------------
def _store() -> StorageManager:
    return StorageManager(current_app.config['DATABASE_PATH'])

# -------------------------------------------------
# Routes
# -------------------------------------------------
@user_bp.route('/')
def dashboard():
    labs = ["physics", "chemistry", "biology"]
    stats = {lab: len(_store().list_items(lab)) for lab in labs}
    return render_template("user/index.html", labs=labs, stats=stats)


@user_bp.route('/lab/<lab_name>')
def lab_view(lab_name):
    items = [{"id": k, **v} for k, v in _store().list_items(lab_name).items()]
    return render_template("user/lab.html", lab_name=lab_name, items=items)


@user_bp.route('/status/<lab_name>/<item_id>')
def status(lab_name, item_id):
    item = _store().list_items(lab_name).get(item_id)
    return render_template("user/status.html", item=item)

@user_bp.route("/qr-demo")
def qr_demo():
    return render_template("qr_demo.html")
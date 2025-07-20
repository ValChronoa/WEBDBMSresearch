# roles/user/blueprint.py
from flask import Blueprint, render_template, session, current_app, request
from core.decorators import role_required
from core.database import StorageManager
from core.decorators import role_required

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
@role_required("user")
def dashboard():
    labs = ["physics", "chemistry", "biology"]
    stats = {lab: len(_store().list_items(lab)) for lab in labs}
    return render_template("user/index.html", labs=labs, stats=stats)


@user_bp.route('/lab/<lab_name>')
@role_required("user")
def lab_view(lab_name):
    items = [{"id": k, **v} for k, v in _store().list_items(lab_name).items()]
    q = request.args.get("q", "").strip().lower()
    if q:
        def matches(item):
            return any(q in str(v).lower() for v in item.values())
        items = [item for item in items if matches(item)]
    return render_template("user/lab.html", lab_name=lab_name, items=items)


@user_bp.route('/status/<lab_name>/<item_id>')
@role_required("user")
def status(lab_name, item_id):
    item = _store().list_items(lab_name).get(item_id)
    return render_template("user/status.html", item=item)

@user_bp.route("/qr-demo")
@role_required("user")
def qr_demo():
    return render_template("qr_demo.html")

@user_bp.route("/receipt/<lab>/<item_id>")
@role_required("user")
def receipt_student(lab, item_id):
    item = _store().list_items(lab).get(item_id)
    if not item or item.get("borrowed_by") != session.get("uid"):
        return "Not your loan", 403
    return render_template("user/receipt.html", item=item)
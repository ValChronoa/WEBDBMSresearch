from flask import Blueprint, redirect, url_for, session, render_template, abort, current_app
from core.decorators import role_required

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
@role_required("user")
def index():
    """Root entry point: auto-route by role."""
    if "uid" not in session:
        return redirect(url_for("auth.login"))

    role = session["role"]
    if role == "admin":
        return redirect(url_for("admin.dashboard"))
    elif role == "technician":
        return redirect(url_for("tech.dashboard"))
    else:                        # student / user
        return redirect(url_for("user.dashboard"))

# --- QR code item detail routes ---
@main_bp.route('/biology/<item_id>')
def biology_item(item_id):
    item = current_app.storage.list_items('biology').get(item_id)
    if not item:
        abort(404)
    return render_template('item_detail.html', item=item, lab='Biology')

@main_bp.route('/chemistry/<item_id>')
def chemistry_item(item_id):
    item = current_app.storage.list_items('chemistry').get(item_id)
    if not item:
        abort(404)
    return render_template('item_detail.html', item=item, lab='Chemistry')

@main_bp.route('/physics/<item_id>')
def physics_item(item_id):
    item = current_app.storage.list_items('physics').get(item_id)
    if not item:
        abort(404)
    return render_template('item_detail.html', item=item, lab='Physics')
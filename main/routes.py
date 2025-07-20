from flask import Blueprint, redirect, url_for, session 
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
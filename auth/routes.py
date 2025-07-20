from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    flash,
    session,
    render_template,
    current_app,
)
from werkzeug.security import check_password_hash
from core.database import StorageManager
from auth.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# ------------------------------------------------------------------
# Helper: give us a StorageManager tied to the live configuration
# ------------------------------------------------------------------
def _users_store() -> StorageManager:
    return StorageManager(current_app.config["USERS_PATH"])


# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------
@auth_bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        store = _users_store()
        uid, user = User.find(username, store=store)

        if user and check_password_hash(user.password_hash, password):
            session.clear()
            session["uid"] = user.id
            session["role"] = user.role
            if user.role == "technician":
                session["lab"] = user.lab

            # Role-based landing
            if user.role == "admin":
                return redirect(url_for("admin.dashboard"))
            elif user.role == "technician":
                return redirect(url_for("tech.dashboard"))
            else:
                return redirect(url_for("user.dashboard"))

        flash("Invalid credentials", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
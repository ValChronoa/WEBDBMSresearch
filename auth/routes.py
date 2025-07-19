from flask import Blueprint, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from auth.models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username, pwd = request.form["username"], request.form["password"]
        uid, data = User.find(username)
        if data and check_password_hash(data["password_hash"], pwd):
            session["uid"] = uid
            session["role"] = data["role"]
            return redirect(url_for("main.index"))
        flash("Invalid credentials", "danger")
    from flask import render_template
    return render_template("login.html")

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
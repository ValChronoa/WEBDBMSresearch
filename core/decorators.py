from functools import wraps
from flask import session, redirect, url_for, flash

def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if "uid" not in session or session.get("role") != role:
                flash("Access denied.", "danger")
                return redirect(url_for("auth.login"))
            return f(*args, **kwargs)
        return wrapped
    return decorator

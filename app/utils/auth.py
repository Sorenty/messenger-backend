from functools import wraps

from flask import flash, g, jsonify, redirect, url_for


def login_required_api(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not getattr(g, "current_user", None):
            return jsonify({"error": "unauthorized"}), 401
        return view(*args, **kwargs)

    return wrapped


def login_required_page(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not getattr(g, "current_user", None):
            flash("Для доступа к этой странице нужно залогиниться", "warning")
            return redirect(url_for("pages.login_page"))
        return view(*args, **kwargs)

    return wrapped
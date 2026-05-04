from functools import wraps
from flask import jsonify, g


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not getattr(g, "current_user", None):
            return jsonify({"error": "unauthorized"}), 401
        return view(*args, **kwargs)

    return wrapped
from flask import Blueprint, render_template, g
from ..utils.auth import login_required

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def index():
    return render_template("index.html")


@pages_bp.route("/chats")
@login_required
def chats():
    user = g.current_user
    return render_template("chats.html", user=user)
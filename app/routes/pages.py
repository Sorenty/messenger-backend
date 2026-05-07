from flask import Blueprint, render_template, g
from ..utils.auth import login_required_page

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def index():
    return render_template("index.html")


@pages_bp.route("/login")
def login_page():
    return render_template("login.html")


@pages_bp.route("/register")
def register_page():
    return render_template("register.html")


@pages_bp.route("/chats")
@login_required_page
def chats():
    return render_template("chats.html", user=g.current_user)


@pages_bp.route("/feed")
@login_required_page
def feed():
    return render_template("feed.html", user=g.current_user)
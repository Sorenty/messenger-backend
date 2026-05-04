from flask import Blueprint, request, jsonify, session
from ..services.user_service import UserService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    if UserService.get_by_email(email):
        return jsonify({"error": "user already exists"}), 409

    user = UserService.create_user(email=email, password=password)
    return jsonify(user.to_dict()), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user = UserService.get_by_email(email)
    if not user or not user.check_password(password):
        return jsonify({"error": "invalid credentials"}), 401

    session["user_id"] = user.id
    session["role"] = user.role
    return jsonify({"message": "logged in", "user": user.to_dict()}), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "logged out"}), 200

@auth_bp.route("/me", methods=["GET"])
def me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "unauthorized"}), 401

    user = UserService.get_by_id(user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404

    return jsonify(user.to_dict()), 200
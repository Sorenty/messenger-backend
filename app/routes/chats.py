from flask import Blueprint, jsonify, request, g
from ..services.chat_service import ChatService

chats_bp = Blueprint("chats", __name__)


def require_user():
    if not g.current_user:
        return jsonify({"error": "unauthorized"}), 401
    return None


@chats_bp.route("", methods=["GET"])
def list_chats():
    unauthorized = require_user()
    if unauthorized:
        return unauthorized

    chats = ChatService.list_user_chats(g.current_user.id)
    return jsonify([chat.to_dict() for chat in chats]), 200


@chats_bp.route("", methods=["POST"])
def create_chat():
    unauthorized = require_user()
    if unauthorized:
        return unauthorized

    data = request.get_json() or {}
    chat_type = data.get("type", "group")
    name = data.get("name")
    member_emails = data.get("member_emails", [])

    if chat_type == "private":
        target_email = data.get("member_email")
        if not target_email:
            return jsonify({"error": "member_email is required"}), 400

        chat = ChatService.create_private_chat(g.current_user, target_email)
        if not chat:
            return jsonify({"error": "target user not found"}), 404

        return jsonify(chat.to_dict()), 201

    # group chat
    if not name:
        return jsonify({"error": "name is required"}), 400

    chat = ChatService.create_group_chat(g.current_user, name, member_emails)
    return jsonify(chat.to_dict()), 201


@chats_bp.route("/<int:chat_id>/messages", methods=["GET"])
def list_chat_messages(chat_id):
    unauthorized = require_user()
    if unauthorized:
        return unauthorized

    if not ChatService.user_in_chat(chat_id, g.current_user.id):
        return jsonify({"error": "forbidden"}), 403

    messages = ChatService.list_messages(chat_id)
    return jsonify([m.to_dict() for m in messages]), 200


@chats_bp.route("/<int:chat_id>/messages", methods=["POST"])
def send_chat_message(chat_id):
    unauthorized = require_user()
    if unauthorized:
        return unauthorized

    if not ChatService.user_in_chat(chat_id, g.current_user.id):
        return jsonify({"error": "forbidden"}), 403

    data = request.get_json() or {}
    text = data.get("text")

    if not text:
        return jsonify({"error": "text is required"}), 400

    msg = ChatService.send_message(chat_id, g.current_user, text)
    return jsonify(msg.to_dict()), 201
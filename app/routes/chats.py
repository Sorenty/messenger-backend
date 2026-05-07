from flask import Blueprint, jsonify, request, g
from ..services.chat_service import ChatService
from ..services.user_service import UserService

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


@chats_bp.route("/users", methods=["GET"])
def list_users():
    unauthorized = require_user()
    if unauthorized:
        return unauthorized

    q = request.args.get("q", "").strip()
    chat_id = request.args.get("chat_id", type=int)

    exclude_ids = [g.current_user.id]

    if chat_id:
        if not ChatService.is_owner(chat_id, g.current_user.id):
            return jsonify({"error": "forbidden"}), 403
        exclude_ids.extend(ChatService.chat_member_ids(chat_id))

    users = UserService.search_users(query=q, exclude_ids=exclude_ids, limit=10)
    return jsonify([u.to_dict() for u in users]), 200


@chats_bp.route("/<int:chat_id>/members", methods=["GET"])
def list_members(chat_id):
    unauthorized = require_user()
    if unauthorized:
        return unauthorized

    if not ChatService.is_owner(chat_id, g.current_user.id):
        return jsonify({"error": "forbidden"}), 403

    members = ChatService.list_members(chat_id)
    return jsonify([m.to_dict() for m in members]), 200


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


@chats_bp.route("/<int:chat_id>/members", methods=["POST"])
def add_chat_member(chat_id):
    unauthorized = require_user()
    if unauthorized:
        return unauthorized

    if not ChatService.is_owner(chat_id, g.current_user.id):
        return jsonify({"error": "forbidden"}), 403

    data = request.get_json() or {}
    email = data.get("email")
    if not email:
        return jsonify({"error": "email is required"}), 400

    status, user = ChatService.add_user_to_chat(chat_id, email)

    if status == "not_found":
        return jsonify({"error": "user not found"}), 404
    if status == "banned":
        return jsonify({"error": "user is banned in this chat"}), 400
    if status == "exists":
        return jsonify({"message": "user already in chat"}), 200

    return jsonify({"message": "member added"}), 200


@chats_bp.route("/<int:chat_id>/members/<int:user_id>", methods=["DELETE"])
def remove_chat_member(chat_id, user_id):
    unauthorized = require_user()
    if unauthorized:
        return unauthorized

    if not ChatService.is_owner(chat_id, g.current_user.id):
        return jsonify({"error": "forbidden"}), 403

    chat = ChatService.get_chat(chat_id)
    if not chat:
        return jsonify({"error": "chat not found"}), 404

    if chat.owner_id == user_id:
        return jsonify({"error": "owner cannot be removed"}), 400

    status = ChatService.remove_member(chat_id, user_id)
    if status == "not_found":
        return jsonify({"error": "member not found"}), 404

    return jsonify({"message": "member removed"}), 200


@chats_bp.route("/<int:chat_id>/members/<int:user_id>/ban", methods=["POST"])
def ban_chat_member(chat_id, user_id):
    unauthorized = require_user()
    if unauthorized:
        return unauthorized

    if not ChatService.is_owner(chat_id, g.current_user.id):
        return jsonify({"error": "forbidden"}), 403

    chat = ChatService.get_chat(chat_id)
    if not chat:
        return jsonify({"error": "chat not found"}), 404

    if chat.owner_id == user_id:
        return jsonify({"error": "owner cannot be banned"}), 400

    status = ChatService.ban_member(chat_id, user_id)
    if status == "not_found":
        return jsonify({"error": "member not found"}), 404
    if status == "already_banned":
        return jsonify({"message": "member already banned"}), 200

    return jsonify({"message": "member banned"}), 200


@chats_bp.route("/<int:chat_id>/members/<int:user_id>/unban", methods=["POST"])
def unban_chat_member(chat_id, user_id):
    unauthorized = require_user()
    if unauthorized:
        return unauthorized

    if not ChatService.is_owner(chat_id, g.current_user.id):
        return jsonify({"error": "forbidden"}), 403

    status = ChatService.unban_member(chat_id, user_id)
    if status == "not_found":
        return jsonify({"error": "member not found"}), 404
    if status == "not_banned":
        return jsonify({"message": "member already active"}), 200

    return jsonify({"message": "member unbanned"}), 200
from flask import Blueprint, request, jsonify
from ..services.message_service import MessageService

channels_bp = Blueprint("channels", __name__)

@channels_bp.route('/<channel>/')
def home():
    return {"message": "Messenger backend is running 🚀"}

@channels_bp.route("/<channel>/messages", methods=["POST"])
def post_message(channel):
    data = request.get_json() or {}
    sender = data.get("sender")
    text = data.get("text")
    if not sender or not text:
        return jsonify({"error": "sender and text are required"}), 400
    msg = MessageService.post_message(channel, sender, text)
    return jsonify(msg.to_dict()), 201

@channels_bp.route("/<channel>/messages", methods=["GET"])
def get_messages(channel):
    limit = int(request.args.get("limit", 100))
    messages = MessageService.get_history(channel, limit=limit)
    return jsonify([m.to_dict() for m in messages]), 200
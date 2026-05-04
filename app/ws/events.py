from flask import request, session
from flask_socketio import join_room, leave_room, emit
from ..services.chat_service import ChatService
from .socketio_instance import socketio


@socketio.on("join_chat")
def handle_join_chat(data):
    chat_id = int(data.get("chat_id"))
    user_id = session.get("user_id")

    if not user_id:
        emit("error", {"error": "unauthorized"})
        return

    if not ChatService.user_in_chat(chat_id, user_id):
        emit("error", {"error": "forbidden"})
        return

    join_room(f"chat:{chat_id}")
    emit("joined_chat", {"chat_id": chat_id})


@socketio.on("leave_chat")
def handle_leave_chat(data):
    chat_id = int(data.get("chat_id"))
    leave_room(f"chat:{chat_id}")
    emit("left_chat", {"chat_id": chat_id})


@socketio.on("send_message")
def handle_send_message(data):
    chat_id = int(data.get("chat_id"))
    text = (data.get("text") or "").strip()
    user_id = session.get("user_id")

    if not user_id:
        emit("error", {"error": "unauthorized"})
        return

    if not text:
        emit("error", {"error": "text is required"})
        return

    if not ChatService.user_in_chat(chat_id, user_id):
        emit("error", {"error": "forbidden"})
        return

    from ..services.user_service import UserService
    user = UserService.get_by_id(user_id)

    msg = ChatService.send_message(chat_id, user, text)

    socketio.emit(
        "new_message",
        {"chat_id": chat_id, "message": msg.to_dict()},
        room=f"chat:{chat_id}",
    )
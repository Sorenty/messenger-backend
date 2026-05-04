from __future__ import annotations

from ..models.chat import Chat
from ..models.membership import Membership
from ..models.message import Message
from ..models.user import User
from ..utils.db import db


class ChatService:
    @staticmethod
    def list_user_chats(user_id: int):
        return (
            Chat.query
            .join(Membership, Membership.chat_id == Chat.id)
            .filter(Membership.user_id == user_id)
            .order_by(Chat.created_at.desc())
            .all()
        )

    @staticmethod
    def get_chat(chat_id: int) -> Chat | None:
        return Chat.query.get(chat_id)

    @staticmethod
    def user_in_chat(chat_id: int, user_id: int) -> bool:
        return Membership.query.filter_by(chat_id=chat_id, user_id=user_id).first() is not None

    @staticmethod
    def create_group_chat(owner: User, name: str, member_emails: list[str]):
        chat = Chat(name=name, is_group=True)
        db.session.add(chat)
        db.session.flush()

        members = {owner.email, *(member_emails or [])}
        for email in members:
            user = User.query.filter_by(email=email).first()
            if not user:
                continue
            db.session.add(Membership(user_id=user.id, chat_id=chat.id))

        db.session.commit()
        return chat

    @staticmethod
    def create_private_chat(owner: User, target_email: str):
        target = User.query.filter_by(email=target_email).first()
        if not target:
            return None

        # простой вариант: ищем чат без is_group и с ровно 2 участниками
        existing = (
            Chat.query
            .join(Membership, Membership.chat_id == Chat.id)
            .filter(Chat.is_group.is_(False))
            .filter(Membership.user_id.in_([owner.id, target.id]))
            .all()
        )

        for chat in existing:
            user_ids = [m.user_id for m in chat.members]
            if sorted(user_ids) == sorted([owner.id, target.id]):
                return chat

        chat = Chat(name=None, is_group=False)
        db.session.add(chat)
        db.session.flush()

        db.session.add(Membership(user_id=owner.id, chat_id=chat.id))
        db.session.add(Membership(user_id=target.id, chat_id=chat.id))
        db.session.commit()
        return chat

    @staticmethod
    def list_messages(chat_id: int):
        return Message.query.filter_by(chat_id=chat_id).order_by(Message.created_at.asc()).all()

    @staticmethod
    def send_message(chat_id: int, user: User, text: str):
        msg = Message(
            chat_id=chat_id,
            sender_id=user.id,
            sender=user.email,
            text=text,
        )
        db.session.add(msg)
        db.session.commit()
        return msg
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
            .filter(Membership.is_banned.is_(False))
            .order_by(Chat.created_at.desc())
            .all()
        )

    @staticmethod
    def get_chat(chat_id: int) -> Chat | None:
        return Chat.query.get(chat_id)

    @staticmethod
    def is_owner(chat_id: int, user_id: int) -> bool:
        chat = Chat.query.get(chat_id)
        return bool(chat and chat.owner_id == user_id)

    @staticmethod
    def user_in_chat(chat_id: int, user_id: int) -> bool:
        return (
            Membership.query
            .filter_by(chat_id=chat_id, user_id=user_id)
            .filter(Membership.is_banned.is_(False))
            .first()
            is not None
        )

    @staticmethod
    def chat_member_ids(chat_id: int) -> list[int]:
        return [m.user_id for m in Membership.query.filter_by(chat_id=chat_id).all()]

    @staticmethod
    def list_members(chat_id: int):
        return (
            Membership.query
            .filter_by(chat_id=chat_id)
            .join(User, User.id == Membership.user_id)
            .order_by(Membership.is_banned.asc(), User.email.asc())
            .all()
        )

    @staticmethod
    def create_group_chat(owner: User, name: str, member_emails: list[str]):
        chat = Chat(name=name, is_group=True, owner_id=owner.id)
        db.session.add(chat)
        db.session.flush()

        members = {owner.email, *(member_emails or [])}
        for email in members:
            user = User.query.filter_by(email=email).first()
            if not user:
                continue

            existing = Membership.query.filter_by(chat_id=chat.id, user_id=user.id).first()
            if existing:
                existing.is_banned = False
                continue

            db.session.add(Membership(user_id=user.id, chat_id=chat.id))

        db.session.commit()
        return chat

    @staticmethod
    def create_private_chat(owner: User, target_email: str):
        target = User.query.filter_by(email=target_email).first()
        if not target:
            return None

        existing = (
            Chat.query
            .join(Membership, Membership.chat_id == Chat.id)
            .filter(Chat.is_group.is_(False))
            .filter(Membership.user_id.in_([owner.id, target.id]))
            .all()
        )

        for chat in existing:
            user_ids = [m.user_id for m in chat.members if not m.is_banned]
            if sorted(user_ids) == sorted([owner.id, target.id]):
                return chat

        chat = Chat(name=None, is_group=False, owner_id=owner.id)
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

    @staticmethod
    def add_user_to_chat(chat_id: int, email: str):
        user = User.query.filter_by(email=email).first()
        if not user:
            return "not_found", None

        membership = Membership.query.filter_by(chat_id=chat_id, user_id=user.id).first()
        if membership:
            if membership.is_banned:
                return "banned", user
            return "exists", user

        db.session.add(Membership(chat_id=chat_id, user_id=user.id))
        db.session.commit()
        return "added", user

    @staticmethod
    def remove_member(chat_id: int, user_id: int):
        membership = Membership.query.filter_by(chat_id=chat_id, user_id=user_id).first()
        if not membership:
            return "not_found"

        db.session.delete(membership)
        db.session.commit()
        return "removed"

    @staticmethod
    def ban_member(chat_id: int, user_id: int):
        membership = Membership.query.filter_by(chat_id=chat_id, user_id=user_id).first()
        if not membership:
            return "not_found"

        if membership.is_banned:
            return "already_banned"

        membership.is_banned = True
        db.session.commit()
        return "banned"

    @staticmethod
    def unban_member(chat_id: int, user_id: int):
        membership = Membership.query.filter_by(chat_id=chat_id, user_id=user_id).first()
        if not membership:
            return "not_found"

        if not membership.is_banned:
            return "not_banned"

        membership.is_banned = False
        db.session.commit()
        return "unbanned"
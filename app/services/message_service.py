from ..models.message import Message
from ..utils.db import db

class MessageService:
    @staticmethod
    def post_message(channel, sender, text):
        msg = Message(channel=channel, sender=sender, text=text)
        db.session.add(msg)
        db.session.commit()
        return msg

    @staticmethod
    def get_history(channel, limit=100):
        return Message.query.filter_by(channel=channel).order_by(Message.created_at.desc()).limit(limit).all()
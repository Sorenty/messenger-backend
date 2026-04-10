import logging
from ..models.message import Message
from ..utils.db import db

logger = logging.getLogger(__name__)

class MessageService:
    @staticmethod
    def post_message(channel, sender, text):
        msg = Message(channel=channel, sender=sender, text=text)
        db.session.add(msg)
        db.session.commit()
        logger.info("message_created", extra={"channel": channel, "sender": sender})
        return msg

    @staticmethod
    def get_history(channel, limit=100):
        logger.info("history_requested", extra={"channel": channel, "limit": limit})
        return Message.query.filter_by(channel=channel).order_by(Message.created_at.desc()).limit(limit).all()
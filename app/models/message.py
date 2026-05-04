from datetime import datetime
from ..utils.db import db


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)

    # старый режим, чтобы не сломать практики
    channel = db.Column(db.String(128), nullable=True)
    sender = db.Column(db.String(128), nullable=True)

    # новый режим для чатов
    chat_id = db.Column(db.Integer, db.ForeignKey("chats.id"), nullable=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    chat = db.relationship("Chat", back_populates="messages")
    sender_user = db.relationship("User")

    def to_dict(self):
        return {
            "id": self.id,
            "channel": self.channel,
            "sender": self.sender,
            "chat_id": self.chat_id,
            "sender_id": self.sender_id,
            "text": self.text,
            "created_at": self.created_at.isoformat(),
        }
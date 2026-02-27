from ..utils.db import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(db.String(128), nullable=False)
    sender = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "channel": self.channel,
            "sender": self.sender,
            "text": self.text,
            "created_at": self.created_at.isoformat()
        }
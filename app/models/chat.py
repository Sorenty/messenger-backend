from datetime import datetime
from ..utils.db import db


class Chat(db.Model):
    __tablename__ = "chats"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    is_group = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    members = db.relationship("Membership", back_populates="chat", cascade="all, delete-orphan")
    messages = db.relationship("Message", back_populates="chat", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_group": self.is_group,
            "created_at": self.created_at.isoformat(),
        }
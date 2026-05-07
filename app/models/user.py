from datetime import datetime
from ..utils.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(32), nullable=False, default="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    memberships = db.relationship("Membership", back_populates="user", cascade="all, delete-orphan")
    owned_chats = db.relationship("Chat", back_populates="owner")
    messages = db.relationship("Message", back_populates="sender_user")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role,
        }
from ..utils.db import db


class Membership(db.Model):
    __tablename__ = "memberships"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey("chats.id"), nullable=False)
    is_banned = db.Column(db.Boolean, nullable=False, default=False)

    user = db.relationship("User", back_populates="memberships")
    chat = db.relationship("Chat", back_populates="members")

    __table_args__ = (
        db.UniqueConstraint("user_id", "chat_id", name="uq_membership_user_chat"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "chat_id": self.chat_id,
            "email": self.user.email if self.user else None,
            "is_banned": self.is_banned,
            "is_owner": bool(self.chat and self.chat.owner_id == self.user_id),
        }
from ..utils.db import db

class Membership(db.Model):
    __tablename__ = "memberships"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey("chats.id"), nullable=False)

    user = db.relationship("User", back_populates="memberships")
    chat = db.relationship("Chat", back_populates="members")

    __table_args__ = (
        db.UniqueConstraint("user_id", "chat_id", name="uq_membership_user_chat"),
    )
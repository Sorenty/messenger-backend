from ..models.user import User
from ..utils.db import db


class UserService:
    @staticmethod
    def create_user(email: str, password: str, role: str = "user") -> User:
        user = User(email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_email(email: str) -> User | None:
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_id(user_id: int) -> User | None:
        return User.query.get(user_id)
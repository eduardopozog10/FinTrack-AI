from sqlmodel import Session, select

from app.auth.security import hash_password
from app.models.user import User
from app.schemas.user import UserRegister


class AuthService:

    @staticmethod
    def register(
        session: Session,
        user: UserRegister,
    ):

        statement = select(User).where(
            User.email == user.email,
        )

        existing_user = session.exec(statement).first()
        if existing_user:
            raise ValueError(
                "Email already registered",
            )
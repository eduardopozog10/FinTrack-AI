from sqlmodel import Session, select

from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.schemas.user import (
    UserRegister,
    UserLogin,
)
from app.models.user import User


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

        db_user = User(
            full_name=user.full_name,
            email=user.email,
            hashed_password=hash_password(user.password),
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user
    

    @staticmethod
    def login(
        session: Session,
        user: UserLogin,
    ):

        statement = select(User).where(
            User.email == user.email,
        )

        db_user = session.exec(statement).first()

        if not db_user:
            raise ValueError("Invalid credentials")

        if not verify_password(
            user.password,
            db_user.hashed_password,
        ):
            raise ValueError("Invalid credentials")

        access_token = create_access_token(
            {
                "sub": db_user.email,
                "user_id": db_user.id,
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
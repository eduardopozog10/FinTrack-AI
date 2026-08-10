from sqlmodel import Session, select

from app.models.user import User


class TelegramUserService:

    @staticmethod
    def get_or_create(
        session: Session,
        telegram_id: int,
        full_name: str,
    ) -> User:

        user = session.exec(
            select(User).where(
                User.telegram_id == telegram_id
            )
        ).first()

        if user is not None:
            return user

        user = User(
            full_name=full_name,
            email=f"telegram_{telegram_id}@fintrack.local",
            hashed_password="TELEGRAM_USER",
            telegram_id=telegram_id,
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        print("========== Telegram User ==========")
        print("Nuevo usuario creado")
        print("User ID:", user.id)
        print("Telegram ID:", telegram_id)
        print("Nombre:", full_name)
        print("===================================")

        return user
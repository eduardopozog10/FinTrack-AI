from sqlmodel import Session, select

from app.models.user import User


class UserProfileService:

    @staticmethod
    def get_user(
        session: Session,
        user_id: int,
    ) -> User | None:

        return session.exec(
            select(User).where(
                User.id == user_id
            )
        ).first()

    @staticmethod
    def update_name(
        session: Session,
        user_id: int,
        full_name: str,
    ) -> User | None:

        user = UserProfileService.get_user(
            session=session,
            user_id=user_id,
        )

        if user is None:
            return None

        full_name = full_name.strip()

        if not full_name:
            return None

        user.full_name = full_name

        session.add(user)
        session.commit()
        session.refresh(user)

        return user
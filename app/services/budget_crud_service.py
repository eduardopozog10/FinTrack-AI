from sqlmodel import Session, select

from app.models.budget import Budget


class BudgetCrudService:

    @staticmethod
    def create(
        session: Session,
        category: str,
        amount: float,
        user_id: int | None = None,
    ):

        budget = Budget(
            category=category,
            amount=amount,
            user_id=user_id,
        )

        session.add(budget)
        session.commit()
        session.refresh(budget)

        return budget

    @staticmethod
    def get_by_category(
        session: Session,
        category: str,
        user_id: int | None = None,
    ):

        return session.exec(
            select(Budget)
            .where(
                Budget.category == category,
                Budget.user_id == user_id,
            )
        ).first()

    @staticmethod
    def update(
        session: Session,
        budget: Budget,
        amount: float,
    ):

        budget.amount = amount

        session.add(budget)
        session.commit()
        session.refresh(budget)

        return budget

    @staticmethod
    def delete(
        session: Session,
        budget: Budget,
    ):

        session.delete(budget)
        session.commit()
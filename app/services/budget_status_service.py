from sqlalchemy import func
from sqlmodel import Session, select

from app.models.budget import Budget
from app.models.transaction import Transaction
from app.constants.transaction_type import TransactionType


class BudgetStatusService:

    @staticmethod
    def get_status(
        session: Session,
        category: str,
        user_id: int | None = None,
    ):

        budget = session.exec(
            select(Budget)
            .where(
                Budget.category == category,
                Budget.user_id == user_id,
            )
        ).first()

        if budget is None:
            return None

        total_spent = session.exec(
            select(func.sum(Transaction.amount))
            .where(
                Transaction.transaction_type == TransactionType.EXPENSE,
                Transaction.category == category,
                Transaction.user_id == user_id,
            )
        ).one()

        total_spent = total_spent or 0

        remaining = budget.amount - total_spent

        percentage = (
            (total_spent / budget.amount) * 100
            if budget.amount > 0
            else 0
        )

        exceeded = total_spent > budget.amount

        return {
            "category": category,
            "budget": budget.amount,
            "spent": total_spent,
            "remaining": remaining,
            "percentage": round(percentage, 1),
            "exceeded": exceeded,
        }
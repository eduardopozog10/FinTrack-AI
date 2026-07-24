from datetime import datetime

from sqlmodel import Session, select
from sqlalchemy import func

from app.models.transaction import Transaction
from app.constants.transaction_type import TransactionType


class TodayExpenseService:

    @staticmethod
    def process(
        session: Session,
    ):

        today = datetime.today().date()

        total = session.exec(
            select(
                func.sum(Transaction.amount)
            )
            .where(
                Transaction.transaction_type == TransactionType.EXPENSE,
            )
            .where(
                func.date(Transaction.created_at) == today,
            )
        ).one()

        return {
            "today_expense": total or 0,
        }
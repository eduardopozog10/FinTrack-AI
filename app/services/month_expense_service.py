from datetime import datetime

from sqlmodel import Session, select
from sqlalchemy import func

from app.models.transaction import Transaction
from app.constants.transaction_type import TransactionType


class MonthExpenseService:

    @staticmethod
    def process(
        session: Session,
    ):

        today = datetime.today()

        total = session.exec(
            select(
                func.sum(Transaction.amount)
            )
            .where(
                Transaction.transaction_type == TransactionType.EXPENSE,
            )
            .where(
                func.extract(
                    "month",
                    Transaction.created_at,
                )
                == today.month,
            )
            .where(
                func.extract(
                    "year",
                    Transaction.created_at,
                )
                == today.year,
            )
        ).one()

        return {
            "month_expense": total or 0,
        }
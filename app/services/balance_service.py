from sqlmodel import Session, select
from sqlalchemy import func

from app.models.transaction import Transaction
from app.constants.transaction_type import TransactionType


class BalanceService:

    @staticmethod
    def process(
        session: Session,
    ):

        total_income = session.exec(
            select(func.sum(Transaction.amount))
            .where(Transaction.transaction_type == TransactionType.INCOME)
        ).one()

        total_expense = session.exec(
            select(func.sum(Transaction.amount))
            .where(Transaction.transaction_type == TransactionType.EXPENSE)
        ).one()

        total_income = total_income or 0
        total_expense = total_expense or 0

        return {
            "income": total_income,
            "expense": total_expense,
            "balance": total_income - total_expense,
        }
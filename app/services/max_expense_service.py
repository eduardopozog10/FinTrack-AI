from sqlmodel import Session, select

from app.models.transaction import Transaction
from app.constants.transaction_type import TransactionType


class MaxExpenseService:

    @staticmethod
    def process(
        session: Session,
    ):

        transaction = session.exec(
            select(Transaction)
            .where(
                Transaction.transaction_type == TransactionType.EXPENSE,
            )
            .order_by(
                Transaction.amount.desc(),
            )
        ).first()

        if transaction is None:
            return {
                "message": "No existen gastos registrados.",
            }

        return {
            "max_expense": {
                "description": transaction.description,
                "amount": transaction.amount,
                "category": transaction.category,
            }
        }
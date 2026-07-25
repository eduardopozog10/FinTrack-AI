from sqlmodel import Session, select

from app.models.transaction import Transaction
from app.constants.transaction_type import TransactionType


class LastExpenseService:

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
                Transaction.created_at.desc(),
            )
        ).first()

        if transaction is None:
            return {
                "message": "No existen gastos registrados.",
            }

        return {
            "last_expense": {
                "description": transaction.description,
                "amount": transaction.amount,
                "category": transaction.category,
            }
        }
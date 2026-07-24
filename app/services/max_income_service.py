from sqlmodel import Session, select

from app.models.transaction import Transaction
from app.constants.transaction_type import TransactionType


class MaxIncomeService:

    @staticmethod
    def process(
        session: Session,
    ):

        transaction = session.exec(
            select(Transaction)
            .where(
                Transaction.transaction_type == TransactionType.INCOME,
            )
            .order_by(
                Transaction.amount.desc(),
            )
        ).first()

        if transaction is None:
            return {
                "message": "No existen ingresos registrados.",
            }

        return {
            "max_income": {
                "description": transaction.description,
                "amount": transaction.amount,
                "category": transaction.category,
            }
        }
from sqlmodel import Session, select

from app.models.transaction import Transaction


class ListTransactionsService:

    @staticmethod
    def process(
        session: Session,
    ):

        transactions = session.exec(
            select(Transaction)
            .order_by(Transaction.created_at.desc())
        ).all()

        return [
            {
                "id": transaction.id,
                "description": transaction.description,
                "amount": transaction.amount,
                "category": transaction.category,
                "transaction_type": transaction.transaction_type,
                "created_at": transaction.created_at,
            }
            for transaction in transactions
        ]
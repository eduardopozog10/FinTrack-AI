from sqlmodel import Session, select

from app.models.transaction import Transaction
from app.schemas.ai_command import AICommand
from app.schemas.operation_result import OperationResult


class ListTransactionsService:

    @staticmethod
    def process(
        session: Session,
        command: AICommand,
        user_id: int | None = None,
    ):

        transactions = session.exec(
            select(Transaction)
            .where(
                Transaction.user_id == user_id
            )
            .order_by(
                Transaction.created_at.desc()
            )
        ).all()

        data = [
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

        return OperationResult(
            success=True,
            action="list_transactions",
            data=data,
        )
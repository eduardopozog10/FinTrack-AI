from sqlmodel import Session, select

from app.models.transaction import Transaction
from app.schemas.ai_command import AICommand
from app.schemas.operation_result import OperationResult


class DeleteTransactionService:

    @staticmethod
    def process(
        session: Session,
        command: AICommand,
        user_id: int | None = None,
    ):

        description = command.description

        if not description:
            return OperationResult(
                success=False,
                action="transaction_deleted",
                data={
                    "message": "No pude determinar qué transacción eliminar."
                },
            )

        transaction = session.exec(
            select(Transaction)
            .where(
                Transaction.user_id == user_id,
                Transaction.description.ilike(
                    f"%{description}%"
                ),
            )
            .order_by(
                Transaction.created_at.desc(),
            )
        ).first()

        if transaction is None:
            return OperationResult(
                success=False,
                action="transaction_deleted",
                data={
                    "message": "No encontré esa transacción."
                },
            )

        description_deleted = transaction.description

        session.delete(transaction)
        session.commit()

        return OperationResult(
            success=True,
            action="transaction_deleted",
            data={
                "description": description_deleted,
            },
        )
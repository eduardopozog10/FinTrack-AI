from datetime import timedelta

from sqlmodel import Session, select

from app.constants.transaction_type import TransactionType
from app.models.transaction import Transaction
from app.schemas.ai_command import AICommand
from app.schemas.operation_result import OperationResult


class UpdateTransactionService:

    @staticmethod
    def process(
        session: Session,
        command: AICommand,
    ):

        update_field = command.update_field
        update_value = command.update_value
        transaction_reference = command.transaction_reference
        transaction_type = command.transaction_type

        query = select(Transaction)

        if transaction_type == "gasto":
            query = query.where(
                Transaction.transaction_type == TransactionType.EXPENSE
            )

        elif transaction_type == "ingreso":
            query = query.where(
                Transaction.transaction_type == TransactionType.INCOME
            )

        # Por ahora seguimos usando la última transacción.
        # Más adelante usaremos transaction_reference.
        transaction = session.exec(
            query.order_by(
                Transaction.created_at.desc()
            )
        ).first()

        if transaction is None:
            return OperationResult(
                success=False,
                action="transaction_updated",
                data={
                    "message": "No encontré ninguna transacción para actualizar."
                },
            )

        if update_field == "amount":
            transaction.amount = float(update_value)

        elif update_field == "description":
            transaction.description = str(update_value)

        elif update_field == "category":
            transaction.category = str(update_value)

        elif update_field == "created_at":

            if str(update_value).lower() == "ayer":
                transaction.created_at = (
                    transaction.created_at - timedelta(days=1)
                )

        session.add(transaction)
        session.commit()
        session.refresh(transaction)

        return OperationResult(
            success=True,
            action="transaction_updated",
            data=transaction,
        )
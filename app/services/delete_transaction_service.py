from sqlmodel import Session, select

from app.constants.transaction_type import TransactionType
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
        transaction_type = command.transaction_type

        # ==========================================
        # VALIDAR DESCRIPCIÓN
        # ==========================================

        if not description:
            return OperationResult(
                success=False,
                action="transaction_deleted",
                data={
                    "message": (
                        "No pude determinar qué transacción eliminar."
                    )
                },
            )

        # ==========================================
        # CONSULTA BASE
        # ==========================================

        query = select(Transaction).where(
            Transaction.user_id == user_id,
            Transaction.description.ilike(
                f"%{description}%"
            ),
        )

        # ==========================================
        # FILTRAR POR TIPO
        # ==========================================

        if transaction_type == "gasto":
            query = query.where(
                Transaction.transaction_type
                == TransactionType.EXPENSE
            )

        elif transaction_type == "ingreso":
            query = query.where(
                Transaction.transaction_type
                == TransactionType.INCOME
            )

        # ==========================================
        # BUSCAR TRANSACCIÓN
        # ==========================================

        transaction = session.exec(
            query.order_by(
                Transaction.created_at.desc()
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

        # Guardamos los datos antes de eliminarla.
        description_deleted = transaction.description
        amount_deleted = transaction.amount

        # ==========================================
        # ELIMINAR
        # ==========================================

        session.delete(transaction)
        session.commit()

        return OperationResult(
            success=True,
            action="transaction_deleted",
            data={
                "description": description_deleted,
                "amount": amount_deleted,
            },
        )
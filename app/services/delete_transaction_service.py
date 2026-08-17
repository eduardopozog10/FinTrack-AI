from sqlmodel import Session, select

from app.constants.transaction_type import TransactionType
from app.models.transaction import Transaction
from app.schemas.ai_command import AICommand
from app.schemas.operation_result import OperationResult
from app.services.ai_memory_service import AIMemoryService


class DeleteTransactionService:

    @staticmethod
    def process(
        session: Session,
        command: AICommand,
        user_id: int | None = None,
        session_id: str | None = None,
    ):

        description = command.description
        transaction_reference = command.transaction_reference
        transaction_type = command.transaction_type

        # ==========================================
        # CONSULTA BASE
        # ==========================================

        query = select(Transaction).where(
            Transaction.user_id == user_id
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
        # RESOLVER REFERENCIA CONVERSACIONAL
        # ==========================================

        resolved_transaction_id = None

        if transaction_reference and session_id is not None:

            resolved_transaction_id = (
                AIMemoryService.resolve_transaction_reference(
                    session_id=session_id,
                    reference=transaction_reference,
                )
            )

        # ==========================================
        # BUSCAR POR ID RESUELTO
        # ==========================================

        if resolved_transaction_id is not None:

            query = query.where(
                Transaction.id == resolved_transaction_id
            )

        # ==========================================
        # BUSCAR POR DESCRIPCIÓN
        # ==========================================

        elif description:

            query = query.where(
                Transaction.description.ilike(
                    f"%{description}%"
                )
            )

        # ==========================================
        # REFERENCIA SEMÁNTICA POR DESCRIPCIÓN
        # ==========================================

        elif transaction_reference:

            reference = (
                transaction_reference
                .strip()
                .lower()
            )

            generic_references = [
                "contexto",
                "ultima",
                "última",
                "ultimo",
                "último",
                "anterior",
                "la anterior",
                "el anterior",
                "primera",
                "primero",
                "la primera",
                "el primero",
                "segunda",
                "segundo",
                "la segunda",
                "el segundo",
                "tercera",
                "tercero",
                "la tercera",
                "el tercero",
            ]

            if reference not in generic_references:

                query = query.where(
                    Transaction.description.ilike(
                        f"%{transaction_reference}%"
                    )
                )

            else:

                return OperationResult(
                    success=False,
                    action="transaction_deleted",
                    data={
                        "message": (
                            "No pude determinar qué "
                            "transacción eliminar."
                        )
                    },
                )

        # ==========================================
        # SIN INFORMACIÓN SUFICIENTE
        # ==========================================

        else:

            return OperationResult(
                success=False,
                action="transaction_deleted",
                data={
                    "message": (
                        "No pude determinar qué "
                        "transacción eliminar."
                    )
                },
            )

        # ==========================================
        # BUSCAR TRANSACCIÓN
        # ==========================================

        transaction = session.exec(
            query.order_by(
                Transaction.created_at.desc()
            )
        ).first()

        # ==========================================
        # TRANSACCIÓN NO ENCONTRADA
        # ==========================================

        if transaction is None:

            return OperationResult(
                success=False,
                action="transaction_deleted",
                data={
                    "message": (
                        "No encontré esa transacción."
                    )
                },
            )

        # ==========================================
        # GUARDAR DATOS ANTES DE ELIMINAR
        # ==========================================

        description_deleted = transaction.description
        amount_deleted = transaction.amount
        transaction_id_deleted = transaction.id

        # ==========================================
        # ELIMINAR
        # ==========================================

        session.delete(transaction)
        session.commit()

        # ==========================================
        # RESPUESTA
        # ==========================================

        return OperationResult(
            success=True,
            action="transaction_deleted",
            data={
                "id": transaction_id_deleted,
                "description": description_deleted,
                "amount": amount_deleted,
            },
        )
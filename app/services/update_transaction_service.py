from datetime import timedelta

from sqlmodel import Session, select

from app.constants.transaction_type import TransactionType
from app.models.transaction import Transaction
from app.schemas.ai_command import AICommand
from app.schemas.operation_result import OperationResult

from app.events.event_bus import EventBus
from app.events.transaction_updated_event import TransactionUpdatedEvent


class UpdateTransactionService:

    @staticmethod
    def process(
        session: Session,
        command: AICommand,
        user_id: int | None = None,
    ):

        update_field = command.update_field
        update_value = command.update_value
        transaction_reference = command.transaction_reference
        transaction_type = command.transaction_type

        # ==========================================
        # CONSULTA BASE DEL USUARIO
        # ==========================================

        query = select(Transaction).where(
            Transaction.user_id == user_id
        )

        # ==========================================
        # FILTRAR POR TIPO DE TRANSACCIÓN
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
        # BUSCAR TRANSACCIÓN POR REFERENCIA
        # ==========================================

        if transaction_reference:

            reference = transaction_reference.strip().lower()

            generic_references = [
                "ultima",
                "última",
                "ultimo",
                "último",
                "anterior",
            ]

            # Si la referencia NO es genérica,
            # buscamos por la descripción.
            if reference not in generic_references:

                query = query.where(
                    Transaction.description.ilike(
                        f"%{transaction_reference}%"
                    )
                )

        # Si existen varias coincidencias,
        # utilizamos la más reciente.
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
                action="transaction_updated",
                data={
                    "message": (
                        "No encontré ninguna transacción "
                        "que coincida con tu solicitud."
                    )
                },
            )

        # ==========================================
        # GUARDAR VALORES ANTERIORES
        # ==========================================

        previous_category = transaction.category
        previous_amount = transaction.amount

        # ==========================================
        # ACTUALIZAR CAMPO
        # ==========================================

        if update_field == "amount":
            transaction.amount = float(update_value)

        elif update_field == "description":
            transaction.description = str(update_value)

        elif update_field == "category":
            transaction.category = str(update_value)

        elif update_field == "created_at":

            if str(update_value).lower() == "ayer":
                transaction.created_at = (
                    transaction.created_at
                    - timedelta(days=1)
                )

        # ==========================================
        # GUARDAR CAMBIOS
        # ==========================================

        session.add(transaction)
        session.commit()
        session.refresh(transaction)

        # ==========================================
        # EVENTO DE ACTUALIZACIÓN
        # ==========================================

        event = TransactionUpdatedEvent(
            transaction=transaction,
            previous_category=previous_category,
            previous_amount=previous_amount,
            metadata={
                "session": session,
                "field": update_field,
            },
        )

        EventBus.dispatch(event)

        # ==========================================
        # RESPUESTA
        # ==========================================

        return OperationResult(
            success=True,
            action="transaction_updated",
            data=transaction,
            metadata=event.metadata,
        )
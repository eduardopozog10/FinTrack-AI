from datetime import timedelta

from sqlmodel import Session, select

from app.constants.transaction_type import TransactionType
from app.models.transaction import Transaction
from app.schemas.ai_command import AICommand
from app.schemas.operation_result import OperationResult

from app.events.event_bus import EventBus
from app.events.transaction_updated_event import TransactionUpdatedEvent
from app.services.ai_memory_service import AIMemoryService


class UpdateTransactionService:

    @staticmethod
    def process(
        session: Session,
        command: AICommand,
        user_id: int | None = None,
        session_id: str | None = None,
    ):

        update_field = command.update_field
        update_value = command.update_value
        transaction_reference = command.transaction_reference
        transaction_type = command.transaction_type

        # ==========================================
        # VALIDAR ACTUALIZACIÓN
        # ==========================================

        if not update_field or update_value is None:

            return OperationResult(
                success=False,
                action="transaction_updated",
                data={
                    "message": (
                        "No pude determinar qué dato "
                        "quieres modificar."
                    )
                },
            )

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

            reference = (
                transaction_reference
                .strip()
                .lower()
            )

            resolved_transaction_id = None

            # ======================================
            # 1. REFERENCIA CONVERSACIONAL
            # ======================================

            if session_id is not None:

                resolved_transaction_id = (
                    AIMemoryService.resolve_transaction_reference(
                        session_id=session_id,
                        reference=reference,
                    )
                )

            # ======================================
            # 2. REFERENCIA SEMÁNTICA EN EL GRUPO
            # ======================================

            if (
                resolved_transaction_id is None
                and session_id is not None
            ):

                transaction_group = (
                    AIMemoryService.get_transaction_group(
                        session_id=session_id,
                    )
                )

                if transaction_group:

                    group_query = (
                        select(Transaction)
                        .where(
                            Transaction.user_id == user_id
                        )
                        .where(
                            Transaction.id.in_(
                                transaction_group
                            )
                        )
                        .where(
                            Transaction.description.ilike(
                                f"%{transaction_reference}%"
                            )
                        )
                    )

                    # Mantener filtro por tipo
                    # también dentro del grupo.
                    if transaction_type == "gasto":

                        group_query = group_query.where(
                            Transaction.transaction_type
                            == TransactionType.EXPENSE
                        )

                    elif transaction_type == "ingreso":

                        group_query = group_query.where(
                            Transaction.transaction_type
                            == TransactionType.INCOME
                        )

                    group_transaction = (
                        session.exec(
                            group_query
                        ).first()
                    )

                    if group_transaction is not None:

                        resolved_transaction_id = (
                            group_transaction.id
                        )

            # ======================================
            # 3. USAR ID RESUELTO
            # ======================================

            if resolved_transaction_id is not None:

                query = query.where(
                    Transaction.id
                    == resolved_transaction_id
                )

            # ======================================
            # 4. FALLBACK: HISTORIAL COMPLETO
            # ======================================

            else:

                query = query.where(
                    Transaction.description.ilike(
                        f"%{transaction_reference}%"
                    )
                )

        # ==========================================
        # EJECUTAR CONSULTA
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

            try:

                transaction.amount = float(
                    update_value
                )

            except (TypeError, ValueError):

                return OperationResult(
                    success=False,
                    action="transaction_updated",
                    data={
                        "message": (
                            "No pude determinar el nuevo monto."
                        )
                    },
                )

        elif update_field == "description":

            transaction.description = str(
                update_value
            ).strip()

        elif update_field == "category":

            transaction.category = str(
                update_value
            ).strip().lower()

        elif update_field == "created_at":

            if str(update_value).lower() == "ayer":

                transaction.created_at = (
                    transaction.created_at
                    - timedelta(days=1)
                )

            else:

                return OperationResult(
                    success=False,
                    action="transaction_updated",
                    data={
                        "message": (
                            "No pude determinar la nueva fecha."
                        )
                    },
                )

        else:

            return OperationResult(
                success=False,
                action="transaction_updated",
                data={
                    "message": (
                        "No pude determinar qué dato "
                        "quieres modificar."
                    )
                },
            )

        # ==========================================
        # GUARDAR CAMBIOS
        # ==========================================

        session.add(transaction)
        session.commit()
        session.refresh(transaction)

        # ==========================================
        # ACTUALIZAR CONTEXTO CONVERSACIONAL
        # ==========================================

        if session_id is not None:

            AIMemoryService.add_recent_transaction(
                session_id=session_id,
                transaction_id=transaction.id,
            )

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
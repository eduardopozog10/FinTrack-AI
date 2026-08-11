from sqlalchemy import func
from sqlmodel import Session, select

from app.constants.transaction_type import TransactionType
from app.models.transaction import Transaction
from app.schemas.ai_command import AICommand
from app.schemas.operation_result import OperationResult
from app.services.ai_memory_service import AIMemoryService


class DeleteAllExpensesService:

    @staticmethod
    def process(
        session: Session,
        command: AICommand,
        user_id: int | None = None,
        session_id: str | None = None,
    ):

        # ==========================================
        # CONTAR GASTOS DEL USUARIO
        # ==========================================

        count = session.exec(
            select(func.count(Transaction.id))
            .where(
                Transaction.user_id == user_id,
                Transaction.transaction_type
                == TransactionType.EXPENSE,
            )
        ).one()

        count = count or 0

        # ==========================================
        # SIN GASTOS
        # ==========================================

        if count == 0:
            return OperationResult(
                success=False,
                action="delete_all_expenses_confirmation",
                data={
                    "message": "No tienes gastos para eliminar.",
                },
            )

        # ==========================================
        # GUARDAR ACCIÓN PENDIENTE
        # ==========================================

        if session_id is not None:
            AIMemoryService.set_pending_action(
                session_id=session_id,
                action="delete_all_expenses",
                data={
                    "user_id": user_id,
                    "count": count,
                },
            )

        # ==========================================
        # PEDIR CONFIRMACIÓN
        # ==========================================

        return OperationResult(
            success=True,
            action="delete_all_expenses_confirmation",
            data={
                "count": count,
            },
        )
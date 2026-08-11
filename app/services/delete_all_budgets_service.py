from sqlalchemy import func
from sqlmodel import Session, select

from app.models.budget import Budget
from app.schemas.ai_command import AICommand
from app.schemas.operation_result import OperationResult
from app.services.ai_memory_service import AIMemoryService


class DeleteAllBudgetsService:

    @staticmethod
    def process(
        session: Session,
        command: AICommand,
        user_id: int | None = None,
        session_id: str | None = None,
    ):

        # ==========================================
        # CONTAR PRESUPUESTOS DEL USUARIO
        # ==========================================

        count = session.exec(
            select(func.count(Budget.id))
            .where(
                Budget.user_id == user_id,
            )
        ).one()

        count = count or 0

        # ==========================================
        # SIN PRESUPUESTOS
        # ==========================================

        if count == 0:
            return OperationResult(
                success=False,
                action="delete_all_budgets_confirmation",
                data={
                    "message": (
                        "No tienes presupuestos para eliminar."
                    ),
                },
            )

        # ==========================================
        # GUARDAR ACCIÓN PENDIENTE
        # ==========================================

        if session_id is not None:
            AIMemoryService.set_pending_action(
                session_id=session_id,
                action="delete_all_budgets",
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
            action="delete_all_budgets_confirmation",
            data={
                "count": count,
            },
        )
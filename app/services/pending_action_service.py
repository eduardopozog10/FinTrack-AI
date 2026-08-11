from sqlmodel import Session, select

from app.constants.transaction_type import TransactionType
from app.models.transaction import Transaction
from app.models.budget import Budget
from app.schemas.operation_result import OperationResult
from app.services.ai_memory_service import AIMemoryService  


class PendingActionService:

    @staticmethod
    def process(
        session: Session,
        session_id: str,
        message: str,
        user_id: int | None = None,
    ):

        pending = AIMemoryService.get_pending_action(
            session_id
        )

        if pending is None:
            return None

        answer = message.strip().lower()

        # ==========================================
        # RESPUESTAS POSITIVAS
        # ==========================================

        positive_answers = [
            "si",
            "sí",
            "s",
            "yes",
            "confirmo",
            "confirmar",
        ]

        # ==========================================
        # RESPUESTAS NEGATIVAS
        # ==========================================

        negative_answers = [
            "no",
            "n",
            "cancelar",
            "cancela",
        ]

        # ==========================================
        # CANCELAR ACCIÓN
        # ==========================================

        if answer in negative_answers:

            AIMemoryService.clear_pending_action(
                session_id
            )

            return OperationResult(
                success=True,
                action="pending_action_cancelled",
                data={
                    "message": "Operación cancelada.",
                },
            )

        # ==========================================
        # RESPUESTA NO RECONOCIDA
        # ==========================================

        if answer not in positive_answers:

            return OperationResult(
                success=False,
                action="pending_action_invalid_response",
                data={
                    "message": "Responde Sí o No para confirmar.",
                },
            )

        # ==========================================
        # ELIMINAR TODOS LOS GASTOS
        # ==========================================

        if pending["action"] == "delete_all_expenses":

            transactions = session.exec(
                select(Transaction).where(
                    Transaction.user_id == user_id,
                    Transaction.transaction_type
                    == TransactionType.EXPENSE,
                )
            ).all()

            count = len(transactions)

            for transaction in transactions:
                session.delete(transaction)

            session.commit()

            AIMemoryService.clear_pending_action(
                session_id
            )

            return OperationResult(
                success=True,
                action="all_expenses_deleted",
                data={
                    "count": count,
                },
            )


        # ==========================================
        # ELIMINAR TODOS LOS PRESUPUESTOS
        # ==========================================

        if pending["action"] == "delete_all_budgets":

            budgets = session.exec(
                select(Budget).where(
                    Budget.user_id == user_id,
                )
            ).all()

            count = len(budgets)

            for budget in budgets:
                session.delete(budget)

            session.commit()

            AIMemoryService.clear_pending_action(
                session_id
            )

            return OperationResult(
                success=True,
                action="all_budgets_deleted",
                data={
                    "count": count,
                },
            )

        # ==========================================
        # ACCIÓN DESCONOCIDA
        # ==========================================

        AIMemoryService.clear_pending_action(
            session_id
        )

        return OperationResult(
            success=False,
            action="pending_action_unknown",
            data={
                "message": "La acción pendiente ya no es válida.",
            },
        )
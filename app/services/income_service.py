from sqlmodel import Session

from app.constants.categories import Category
from app.models.transaction import TransactionType
from app.schemas.ai_command import AICommand
from app.schemas.operation_result import OperationResult
from app.services.transaction_service import TransactionService
from app.services.ai_memory_service import AIMemoryService


class IncomeService:

    @staticmethod
    def process(
        session: Session,
        command: AICommand,
        user_id: int | None = None,
        session_id: str | None = None,
    ):

        amount = command.amount
        category = command.category
        description = command.description

        if category is None:
            category = Category.OTHER

        if not description:
            description = "Ingreso"

        transaction = TransactionService.create_from_message(
            session=session,
            amount=amount,
            category=category,
            description=description,
            transaction_type=TransactionType.INCOME,
            user_id=user_id,
        )

        # ==========================================
        # ACTUALIZAR CONTEXTO CONVERSACIONAL
        # ==========================================

        if session_id is not None:

            AIMemoryService.add_recent_transaction(
                session_id=session_id,
                transaction_id=transaction.id,
            )

        return OperationResult(
            success=True,
            action="income_created",
            data=transaction,
        )
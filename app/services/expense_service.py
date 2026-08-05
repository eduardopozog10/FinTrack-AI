from sqlmodel import Session

from app.constants.categories import Category
from app.models.transaction import TransactionType
from app.schemas.ai_command import AICommand
from app.schemas.operation_result import OperationResult
from app.services.transaction_service import TransactionService


class ExpenseService:

    @staticmethod
    def process(
        session: Session,
        command: AICommand,
    ):

        amount = command.amount
        category = command.category
        description = command.description

        if category is None:
            category = Category.OTHER

        if not description:
            description = "Gasto"

        transaction = TransactionService.create_from_message(
            session=session,
            amount=amount,
            category=category,
            description=description,
            transaction_type=TransactionType.EXPENSE,
        )

        return OperationResult(
            success=True,
            action="expense_created",
            data=transaction,
        )
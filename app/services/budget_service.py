from sqlmodel import Session

from app.schemas.ai_command import AICommand
from app.schemas.operation_result import OperationResult
from app.services.budget_crud_service import BudgetCrudService


class BudgetService:

    @staticmethod
    def process(
        session: Session,
        command: AICommand,
    ):

        budget = BudgetCrudService.get_by_category(
            session=session,
            category=command.category,
        )

        if budget is None:

            budget = BudgetCrudService.create(
                session=session,
                category=command.category,
                amount=command.amount,
            )

            return OperationResult(
                success=True,
                action="budget_created",
                data=budget,
            )

        budget = BudgetCrudService.update(
            session=session,
            budget=budget,
            amount=command.amount,
        )

        return OperationResult(
            success=True,
            action="budget_updated",
            data=budget,
        )
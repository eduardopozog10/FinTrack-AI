from sqlmodel import Session

from app.schemas.ai_command import AICommand
from app.schemas.operation_result import OperationResult
from app.services.budget_crud_service import BudgetCrudService
from app.services.category_normalizer_service import CategoryNormalizerService


class BudgetService:

    @staticmethod
    def process(
        session: Session,
        command: AICommand,
        user_id: int | None = None,
    ):

        budget = BudgetCrudService.get_by_category(
            session=session,
            category = CategoryNormalizerService.normalize(
                command.category
            ),
            user_id=user_id,
        )

        if budget is None:

            budget = BudgetCrudService.create(
                session=session,
                category=command.category,
                amount=command.amount,
                user_id=user_id,
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
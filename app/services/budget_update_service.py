from sqlmodel import Session

from app.schemas.ai_command import AICommand
from app.schemas.operation_result import OperationResult
from app.services.budget_crud_service import BudgetCrudService
from app.services.category_normalizer_service import CategoryNormalizerService


class BudgetUpdateService:

    @staticmethod
    def process(
        session: Session,
        command: AICommand,
        user_id: int | None = None,
    ):

        category = CategoryNormalizerService.normalize(
            command.category
        )

        if not category:
            return OperationResult(
                success=False,
                action="budget_updated",
                data={
                    "message": (
                        "No pude determinar qué presupuesto quieres actualizar."
                    )
                },
            )

        if command.amount is None:
            return OperationResult(
                success=False,
                action="budget_updated",
                data={
                    "message": (
                        "No pude determinar el nuevo monto del presupuesto."
                    )
                },
            )

        budget = BudgetCrudService.get_by_category(
            session=session,
            category=category,
            user_id=user_id,
        )

        if budget is None:
            return OperationResult(
                success=False,
                action="budget_updated",
                data={
                    "message": (
                        f"No tienes un presupuesto configurado "
                        f"para {category}."
                    )
                },
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
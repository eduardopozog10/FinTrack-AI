from sqlmodel import Session

from app.schemas.ai_command import AICommand
from app.schemas.operation_result import OperationResult
from app.services.budget_crud_service import BudgetCrudService
from app.services.category_normalizer_service import CategoryNormalizerService


class BudgetDeleteService:

    @staticmethod
    def process(
        session: Session,
        command: AICommand,
        user_id: int | None = None,
    ):

        category = CategoryNormalizerService.normalize_budget(
            command.category
        )

        # ==========================================
        # VALIDAR CATEGORÍA
        # ==========================================

        if not category:
            return OperationResult(
                success=False,
                action="budget_deleted",
                data={
                    "message": (
                        "No pude determinar qué presupuesto "
                        "quieres eliminar."
                    )
                },
            )

        # ==========================================
        # BUSCAR PRESUPUESTO DEL USUARIO
        # ==========================================

        budget = BudgetCrudService.get_by_category(
            session=session,
            category=category,
            user_id=user_id,
        )

        if budget is None:
            return OperationResult(
                success=False,
                action="budget_deleted",
                data={
                    "message": (
                        f"No tienes un presupuesto configurado "
                        f"para {category}."
                    )
                },
            )

        # Guardamos la categoría antes de eliminar
        deleted_category = budget.category

        # ==========================================
        # ELIMINAR PRESUPUESTO
        # ==========================================

        BudgetCrudService.delete(
            session=session,
            budget=budget,
        )

        return OperationResult(
            success=True,
            action="budget_deleted",
            data={
                "category": deleted_category,
            },
        )
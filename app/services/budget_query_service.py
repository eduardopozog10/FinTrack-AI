from sqlmodel import Session, select

from app.models.budget import Budget
from app.models.transaction import Transaction
from app.constants.transaction_type import TransactionType
from app.schemas.ai_command import AICommand
from app.schemas.operation_result import OperationResult


class BudgetQueryService:

    @staticmethod
    def process(
        session: Session,
        command: AICommand,
        user_id: int | None = None,
    ):

        category = command.category

        # ==========================================
        # PRESUPUESTO DE UNA CATEGORÍA
        # ==========================================

        if category:

            budget = session.exec(
                select(Budget).where(
                    Budget.category == category,
                    Budget.user_id == user_id,
                )
            ).first()

            if budget is None:
                return OperationResult(
                    success=False,
                    action="budget_status",
                    data={
                        "message": (
                            f"No tienes un presupuesto configurado "
                            f"para {category}."
                        )
                    },
                )

            spent = session.exec(
                select(Transaction.amount).where(
                    Transaction.transaction_type
                    == TransactionType.EXPENSE,
                    Transaction.category == category,
                    Transaction.user_id == user_id,
                )
            ).all()

            total_spent = sum(spent)

            remaining = budget.amount - total_spent

            percentage = (
                (total_spent / budget.amount) * 100
                if budget.amount > 0
                else 0
            )

            return OperationResult(
                success=True,
                action="budget_status",
                data={
                    "category": category,
                    "budget": budget.amount,
                    "spent": total_spent,
                    "remaining": remaining,
                    "percentage": round(percentage, 1),
                    "exceeded": total_spent > budget.amount,
                },
            )

        # ==========================================
        # TODOS LOS PRESUPUESTOS
        # ==========================================

        budgets = session.exec(
            select(Budget).where(
                Budget.user_id == user_id
            )
        ).all()

        if not budgets:
            return OperationResult(
                success=False,
                action="budget_status_all",
                data={
                    "message": "No tienes presupuestos configurados."
                },
            )

        results = []

        for budget in budgets:

            spent = session.exec(
                select(Transaction.amount).where(
                    Transaction.transaction_type
                    == TransactionType.EXPENSE,
                    Transaction.category == budget.category,
                    Transaction.user_id == user_id,
                )
            ).all()

            total_spent = sum(spent)

            remaining = budget.amount - total_spent

            percentage = (
                (total_spent / budget.amount) * 100
                if budget.amount > 0
                else 0
            )

            results.append({
                "category": budget.category,
                "budget": budget.amount,
                "spent": total_spent,
                "remaining": remaining,
                "percentage": round(percentage, 1),
                "exceeded": total_spent > budget.amount,
            })

        return OperationResult(
            success=True,
            action="budget_status_all",
            data=results,
        )
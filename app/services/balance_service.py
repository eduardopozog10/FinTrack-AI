from sqlmodel import Session, select
from sqlalchemy import func

from app.models.transaction import Transaction
from app.constants.transaction_type import TransactionType
from app.schemas.ai_command import AICommand
from app.schemas.operation_result import OperationResult


class BalanceService:

    @staticmethod
    def process(
        session: Session,
        command: AICommand,
        user_id: int | None = None,
    ):

        total_income = session.exec(
            select(func.sum(Transaction.amount))
            .where(
                Transaction.transaction_type == TransactionType.INCOME,
                Transaction.user_id == user_id,
            )
        ).one()

        total_expense = session.exec(
            select(func.sum(Transaction.amount))
            .where(
                Transaction.transaction_type == TransactionType.EXPENSE,
                Transaction.user_id == user_id,
            )
        ).one()

        total_income = total_income or 0
        total_expense = total_expense or 0

        return OperationResult(
            success=True,
            action="balance",
            data={
                "income": total_income,
                "expense": total_expense,
                "balance": total_income - total_expense,
            },
        )
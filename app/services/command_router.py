from sqlmodel import Session

from app.constants.intents import Intent
from app.constants.transaction_type import TransactionType

from app.services.expense_service import ExpenseService
from app.services.income_service import IncomeService
from app.services.balance_service import BalanceService
from app.services.list_transactions_service import ListTransactionsService
from app.services.query_service import QueryService
from app.services.update_transaction_service import UpdateTransactionService
from app.services.delete_transaction_service import DeleteTransactionService

class CommandRouter:

    @staticmethod
    def route(
        session: Session,
        intent: Intent,
        query_type: str,
        amount: float,
        category: str,
        description: str,
    ):

        if intent == Intent.EXPENSE:
            return ExpenseService.process(
                session=session,
                amount=amount,
                category=category,
                description=description,
            )

        if intent == Intent.INCOME:
            return IncomeService.process(
                session=session,
                amount=amount,
                category=category,
                description=description,
            )

        if intent == Intent.BALANCE:
            return BalanceService.process(
                session=session,
            )

        if intent == Intent.LIST:
            return ListTransactionsService.process(
                session=session,
            )

        if intent == Intent.QUERY:

            if query_type == "TOTAL_EXPENSE":
                return QueryService.process(
                    session=session,
                    category=category,
                    transaction_type=TransactionType.EXPENSE,
                )

            if query_type == "TOTAL_INCOME":
                return QueryService.process(
                    session=session,
                    category=category,
                    transaction_type=TransactionType.INCOME,
                )

        if intent == Intent.UPDATE:
            return UpdateTransactionService.process(
                session=session,
                description=description,
                amount=amount,
            )

        if intent == Intent.DELETE:
            return DeleteTransactionService.process(
                session=session,
                description=description,
            )

        return {
            "message": "Comando aún no implementado.",
            "intent": intent,
        }
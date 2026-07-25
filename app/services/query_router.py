from sqlmodel import Session

from app.constants.transaction_type import TransactionType

from app.services.query_service import QueryService
from app.services.today_expense_service import TodayExpenseService
from app.services.month_expense_service import MonthExpenseService
from app.services.month_income_service import MonthIncomeService
from app.services.max_expense_service import MaxExpenseService
from app.services.max_income_service import MaxIncomeService
from app.services.last_expense_service import LastExpenseService
from app.services.last_income_service import LastIncomeService


class QueryRouter:

    @staticmethod
    def route(
        session: Session,
        query_type: str,
        category: str,
    ):

        if query_type == "TODAY_EXPENSE":
            return TodayExpenseService.process(
                session=session,
            )

        if query_type == "MONTH_EXPENSE":
            return MonthExpenseService.process(
                session=session,
            )

        if query_type == "MONTH_INCOME":
            return MonthIncomeService.process(
                session=session,
            )

        if query_type == "MAX_EXPENSE":
            return MaxExpenseService.process(
                session=session,
            )

        if query_type == "MAX_INCOME":
            return MaxIncomeService.process(
                session=session,
            )

        if query_type == "LAST_EXPENSE":
            return LastExpenseService.process(
                session=session,
            )

        if query_type == "LAST_INCOME":
            return LastIncomeService.process(
                session=session,
            )

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

        return {
            "message": "Consulta no implementada.",
            "query": query_type,
        }
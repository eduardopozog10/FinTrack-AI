from sqlmodel import Session

from app.services.max_expense_service import MaxExpenseService
from app.services.max_income_service import MaxIncomeService
from app.services.last_expense_service import LastExpenseService
from app.services.last_income_service import LastIncomeService
from app.services.universal_query_service import UniversalQueryService

class QueryRouter:

    @staticmethod
    def route(
        session: Session,
        query_filter,
    ):

        query_type = query_filter.action

        if query_type == "TODAY_EXPENSE":
            return UniversalQueryService.process(
                session=session,
                query_filter=query_filter,
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
            return UniversalQueryService.process(
                session=session,
                query_filter=query_filter,
            )

        if query_type == "TOTAL_INCOME":
            return UniversalQueryService.process(
                session=session,
                query_filter=query_filter,
            )

        return {
            "message": "Consulta no implementada.",
            "query": query_type,
        }
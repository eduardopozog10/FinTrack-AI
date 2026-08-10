from sqlmodel import Session

from app.schemas.ai_command import AICommand
from app.services.universal_query_service import UniversalQueryService


class QueryRouter:

    @staticmethod
    def process(
        session: Session,
        command: AICommand,
        user_id: int | None = None,
    ):

        query_filter = command.query_filter

        if query_filter is None:
            return {
                "message": "No se pudo determinar la consulta."
            }

        return QueryRouter.route(
            session=session,
            query_filter=query_filter,
            user_id=user_id,
        )

    @staticmethod
    def route(
        session: Session,
        query_filter,
        user_id: int | None = None,
    ):

        query_type = query_filter.action

        if query_type in [
            "TODAY_EXPENSE",
            "MONTH_EXPENSE",
            "MONTH_INCOME",
            "MAX_EXPENSE",
            "MAX_INCOME",
            "LAST_EXPENSE",
            "LAST_INCOME",
            "TOTAL_EXPENSE",
            "TOTAL_INCOME",
            "EXPENSE_HISTORY",
        ]:
            return UniversalQueryService.process(
                session=session,
                query_filter=query_filter,
                user_id=user_id,
            )

        return {
            "message": "Consulta no implementada.",
            "query": query_type,
        }   
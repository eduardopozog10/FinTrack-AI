from sqlmodel import Session

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
            return UniversalQueryService.process(
                session=session,
                query_filter=query_filter,
            )

        if query_type == "MONTH_INCOME":
            return UniversalQueryService.process(
                session=session,
                query_filter=query_filter,
            )
        if query_type == "MAX_EXPENSE":
            return UniversalQueryService.process(
                session=session,
                query_filter=query_filter,
            )

        if query_type == "MAX_INCOME":
            return UniversalQueryService.process(
                session=session,
                query_filter=query_filter,
            )

        if query_type == "LAST_EXPENSE":
            return UniversalQueryService.process(
                session=session,
                query_filter=query_filter,
            )

        if query_type == "LAST_INCOME":
            return UniversalQueryService.process(
                session=session,
                query_filter=query_filter,
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

        if query_type == "EXPENSE_HISTORY":
            return UniversalQueryService.process(
                session=session,
                query_filter=query_filter,
            )

        return {
            "message": "Consulta no implementada.",
            "query": query_type,
        }
from app.schemas.query_filter import QueryFilter
from app.constants.transaction_type import TransactionType


class TransactionFilterBuilder:

    @staticmethod
    def build(
        query_type: str,
        transaction_type,
        category: str | None,
        period: str | None,
    ) -> QueryFilter:

        if query_type == "EXPENSE_HISTORY":
            transaction_type = TransactionType.EXPENSE

        if query_type == "INCOME_HISTORY":
            transaction_type = TransactionType.INCOME

        return QueryFilter(
            action=query_type,
            transaction_type=transaction_type,
            category=category,
            period=period,
        )
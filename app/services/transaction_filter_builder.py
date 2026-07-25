from app.schemas.query_filter import QueryFilter


class TransactionFilterBuilder:

    @staticmethod
    def build(
        query_type: str,
        transaction_type,
        category: str | None,
        period: str | None,
    ) -> QueryFilter:

        return QueryFilter(
            action=query_type,
            transaction_type=transaction_type,
            category=category,
            period=period,
        )
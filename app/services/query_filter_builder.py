from app.schemas.query_filter import QueryFilter
from app.constants.transaction_type import TransactionType


class QueryFilterBuilder:

    @staticmethod
    def build(
        query_type: str,
        transaction_type: TransactionType,
        category: str,
        period: str,
    ):

        return QueryFilter(
            action=query_type,
            transaction_type=transaction_type,
            category=category,
            period=period,
        )
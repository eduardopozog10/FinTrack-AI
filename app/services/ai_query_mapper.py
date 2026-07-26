from app.schemas.ai_analysis import AIAnalysis
from app.schemas.query_filter import QueryFilter

from app.constants.transaction_type import TransactionType

from app.services.transaction_filter_builder import TransactionFilterBuilder


class AIQueryMapper:

    PERIOD_MAP = {
        "hoy": "TODAY",
        "esta semana": "WEEK",
        "este mes": "MONTH",
        "este año": "YEAR",
    }

    @staticmethod
    def build(analysis: AIAnalysis) -> QueryFilter:

        transaction_type = None

        if analysis.tipo_transaccion == "gasto":
            transaction_type = TransactionType.EXPENSE

        elif analysis.tipo_transaccion == "ingreso":
            transaction_type = TransactionType.INCOME

        query_type = analysis.query_type

        period = None

        if analysis.fecha_mencionada:
            period = AIQueryMapper.PERIOD_MAP.get(
                analysis.fecha_mencionada.lower()
            )

        category = analysis.categoria_probable

        return TransactionFilterBuilder.build(
            query_type=query_type,
            transaction_type=transaction_type,
            category=category,
            period=period,
        )
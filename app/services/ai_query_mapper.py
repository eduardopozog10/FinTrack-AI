from app.schemas.ai_analysis import AIAnalysis
from app.schemas.query_filter import QueryFilter

from app.constants.transaction_type import TransactionType


class AIQueryMapper:

    @staticmethod
    def build(analysis: AIAnalysis) -> QueryFilter:
        pass
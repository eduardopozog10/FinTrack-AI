from app.constants.intents import Intent
from app.schemas.ai_analysis import AIAnalysis


class AICommandAdapter:

    @staticmethod
    def adapt(analysis: AIAnalysis):
        intent = Intent.UNKNOWN

        if analysis.intencion_usuario == "registrar_gasto":
            intent = Intent.EXPENSE

        elif analysis.intencion_usuario == "registrar_ingreso":
            intent = Intent.INCOME

        elif analysis.intencion_usuario == "consultar_balance":
            intent = Intent.BALANCE

        elif analysis.intencion_usuario in [
            "consultar_gastos",
            "consultar_ingresos",
            "consultar_categoria",
        ]:
            intent = Intent.QUERY

        return {
            "intent": intent,
            "query_filter": None,
            "amount": None,
            "category": None,
            "description": None,
        }
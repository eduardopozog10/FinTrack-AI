from app.constants.intents import Intent

from app.schemas.ai_analysis import AIAnalysis
from app.schemas.ai_command import AICommand
from app.services.ai_query_mapper import AIQueryMapper


class AICommandAdapter:

    @staticmethod
    def adapt(
        analysis: AIAnalysis,
    ) -> AICommand:

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

        elif analysis.intencion_usuario == "actualizar_transaccion":
            intent = Intent.UPDATE

        elif analysis.intencion_usuario == "crear_presupuesto":
            intent = Intent.BUDGET

        query_filter = None

        if intent == Intent.QUERY:
            query_filter = AIQueryMapper.build(analysis)

        return AICommand(
            intent=intent,
            query_filter=query_filter,
            amount=analysis.monto,
            category=analysis.categoria_probable,
            description=analysis.descripcion,
            transaction_type=analysis.tipo_transaccion,
            update_field=analysis.campo_actualizar,
            update_value=analysis.nuevo_valor,
            transaction_reference=analysis.referencia_transaccion,
        )
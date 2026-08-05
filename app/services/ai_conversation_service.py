from app.schemas.conversation_context import ConversationContext
from app.services.gemini_service import GeminiService
from app.services.template_response_service import TemplateResponseService


class AIConversationService:

    @staticmethod
    def generate_response(
        context: ConversationContext,
    ) -> str:

        print("========== AIConversationService ==========")
        print("Action:", context.action)
        print("==========================================")

        if context.action in [
            "expense_created",
            "income_created",
            "transaction_updated",
            "transaction_deleted",
            "budget_created",
            "budget_updated",
            "balance",
            "today_expense",
            "month_expense",
            "month_income",
        ]:

            print("Usando TemplateResponseService")

            return TemplateResponseService.build(context)

        if context.action in [
            "total_expense",
            "total_income",
            "max_expense",
            "max_income",
            "last_expense",
            "last_income",
            "expense_history",
        ]:

            print("Llamando a Gemini (query)...")

            response = GeminiService.generate_response(context)

            print("Gemini respondió (query)")

            return response

        print("No pasó por ningún generador")

        return "Operación realizada correctamente."
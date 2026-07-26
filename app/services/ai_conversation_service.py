from app.schemas.conversation_context import ConversationContext


class AIConversationService:

    @staticmethod
    def generate_response(
        context: ConversationContext,
    ) -> str:

        if context.action == "expense_created":
            return "✅ Tu gasto fue registrado correctamente."

        if context.action == "income_created":
            return "✅ Tu ingreso fue registrado correctamente."

        return "Operación realizada correctamente."
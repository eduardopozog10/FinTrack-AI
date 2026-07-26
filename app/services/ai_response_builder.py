from app.constants.intents import Intent

from app.schemas.ai_command import AICommand
from app.schemas.ai_response import AIResponse
from app.schemas.conversation_context import ConversationContext
from app.services.ai_conversation_service import AIConversationService


class AIResponseBuilder:

    @staticmethod
    def build(
        command: AICommand,
        result,
        user_message: str,
    ) -> AIResponse:

        if command.intent == Intent.EXPENSE:

            context = ConversationContext(
                action="expense_created",
                success=True,
                user_message=user_message,
                data=result,
            )
            message = AIConversationService.generate_response(
                context
            )

            return AIResponse(
                success=True,
                message=message,
                data=result,
            )

        if command.intent == Intent.INCOME:
            return AIResponse(
                success=True,
                message=(
                    f"✅ Registré un ingreso de "
                    f"${result.amount:,.0f} por "
                    f"{result.description}."
                ),
                data=result,
            )

        return AIResponse(
            success=True,
            message="Operación realizada correctamente.",
            data=result,
        )
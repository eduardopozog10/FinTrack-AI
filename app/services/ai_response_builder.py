from app.constants.intents import Intent

from app.schemas.ai_command import AICommand
from app.schemas.ai_response import AIResponse
from app.schemas.operation_result import OperationResult
from app.services.ai_context_builder import AIContextBuilder
from app.services.ai_conversation_service import AIConversationService


class AIResponseBuilder:

    @staticmethod
    def build(
        command: AICommand,
        result,
        user_message: str,
    ) -> AIResponse:

        # Nueva arquitectura (OperationResult)
        if isinstance(result, OperationResult):

            context = AIContextBuilder.build(
                result=result,
                user_message=user_message,
            )

            context.metadata = result.metadata
            context.success = result.success

            message = AIConversationService.generate_response(
                context
            )

            return AIResponse(
                success=result.success,
                message=message,
                data=result.data,
            )

        # Compatibilidad con servicios antiguos
        if command.intent == Intent.QUERY:

            context = AIContextBuilder.build(
                action=command.query_filter.action.lower(),
                user_message=user_message,
                result=result,
            )

            message = AIConversationService.generate_response(
                context
            )

            return AIResponse(
                success=True,
                message=message,
                data=result,
            )

        return AIResponse(
            success=True,
            message="Operación realizada correctamente.",
            data=result,
        )
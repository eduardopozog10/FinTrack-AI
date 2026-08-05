from app.schemas.conversation_context import ConversationContext
from app.schemas.operation_result import OperationResult


class AIContextBuilder:

    @staticmethod
    def build(
        result: OperationResult,
        user_message: str,
    ) -> ConversationContext:

        return ConversationContext(
            action=result.action,
            success=result.success,
            user_message=user_message,
            data=result.data,
            metadata=result.metadata,
        )
from app.services.gemini_service import GeminiService


class GeneralConversationService:

    @staticmethod
    def process(
        message: str,
        history: list | None = None,
        user_name: str | None = None,
    ) -> str:

        if history is None:
            history = []

        return GeminiService.generate_general_response(
            message=message,
            history=history,
            user_name=user_name,
        )
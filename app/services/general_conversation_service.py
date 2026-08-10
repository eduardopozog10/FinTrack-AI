from app.services.gemini_service import GeminiService


class GeneralConversationService:

    @staticmethod
    def process(
        message: str,
        history: list | None = None,
    ) -> str:

        if history is None:
            history = []

        return GeminiService.generate_general_response(
            message=message,
            history=history,
        )
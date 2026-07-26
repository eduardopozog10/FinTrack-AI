from sqlmodel import Session

from app.services.ai_command_adapter import AICommandAdapter
from app.services.command_router import CommandRouter
from app.services.gemini_service import GeminiService
from app.services.ai_response_builder import AIResponseBuilder


class AIOrchestrator:

    @staticmethod
    def process(
        session: Session,
        message: str,
    ):

        analysis = GeminiService.analyze_message(message)

        command = AICommandAdapter.adapt(analysis)

        result = CommandRouter.route(
            session=session,
            intent=command.intent,
            query_filter=command.query_filter,
            amount=command.amount,
            category=command.category,
            description=command.description,
        )

        return AIResponseBuilder.build(
            command=command,
            result=result,
            user_message=message,
        )
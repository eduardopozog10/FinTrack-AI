from sqlmodel import Session

from app.services.ai_command_adapter import AICommandAdapter
from app.services.command_router import CommandRouter
from app.services.gemini_service import GeminiService
from app.services.ai_response_builder import AIResponseBuilder
from app.services.ai_memory_service import AIMemoryService

class AIOrchestrator:

    @staticmethod
    def process(
        session: Session,
        message: str,
    ):

        session_id = "default"

        history = AIMemoryService.get_history(session_id)

        analysis = GeminiService.analyze_message(
            message=message,
            history=history,
        )

        command = AICommandAdapter.adapt(analysis)

        result = CommandRouter.route(
            session=session,
            command=command,
        )

        response = AIResponseBuilder.build(
            command=command,
            result=result,
            user_message=message,
        )

        AIMemoryService.add(
            session_id=session_id,
            role="user",
            message=message,
        )

        AIMemoryService.add(
            session_id=session_id,
            role="assistant",
            message=response.message,
        )

        return response
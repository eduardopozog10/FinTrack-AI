from sqlmodel import Session

from app.services.ai_command_adapter import AICommandAdapter
from app.services.command_router import CommandRouter
from app.services.gemini_service import GeminiService
from app.services.ai_response_builder import AIResponseBuilder
from app.services.ai_memory_service import AIMemoryService
from app.constants.intents import Intent
from app.services.general_conversation_service import GeneralConversationService
from app.schemas.ai_response import AIResponse


class AIOrchestrator:

    @staticmethod
    def process(
        session: Session,
        message: str,
        session_id: str = "default",
        user_id: int | None = None,
    ):

        history = AIMemoryService.get_history(session_id)

        # ==========================================
        # ANALIZAR MENSAJE
        # ==========================================

        analysis = GeminiService.analyze_message(
            message=message,
            history=history,
        )

        command = AICommandAdapter.adapt(analysis)

        # ==========================================
        # CONVERSACIÓN GENERAL
        # ==========================================

        if command.intent == Intent.UNKNOWN:

            general_response = GeneralConversationService.process(
                message=message,
                history=history,
            )

            AIMemoryService.add(
                session_id=session_id,
                role="user",
                message=message,
            )

            AIMemoryService.add(
                session_id=session_id,
                role="assistant",
                message=general_response,
            )

            return AIResponse(
                success=True,
                message=general_response,
                data=None,
            )

        # ==========================================
        # OPERACIÓN FINANCIERA
        # ==========================================

        result = CommandRouter.route(
            session=session,
            command=command,
            user_id=user_id,
        )

        response = AIResponseBuilder.build(
            command=command,
            result=result,
            user_message=message,
        )

        # ==========================================
        # GUARDAR EN MEMORIA
        # ==========================================

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
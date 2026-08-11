from sqlmodel import Session

from app.services.ai_command_adapter import AICommandAdapter
from app.services.command_router import CommandRouter
from app.services.gemini_service import GeminiService
from app.services.ai_response_builder import AIResponseBuilder
from app.services.ai_memory_service import AIMemoryService
from app.services.pending_action_service import PendingActionService
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
        # COMPROBAR ACCIÓN PENDIENTE
        # ==========================================

        pending_action = AIMemoryService.get_pending_action(
            session_id
        )

        if pending_action is not None:

            result = PendingActionService.process(
                session=session,
                session_id=session_id,
                message=message,
                user_id=user_id,
            )

            # Esta respuesta NO pasa por Gemini.
            if result is not None:

                if result.action == "all_expenses_deleted":

                    count = result.data["count"]

                    if count == 1:
                        response_message = (
                            "🗑️ Listo. Eliminé tu gasto."
                        )
                    else:
                        response_message = (
                            f"🗑️ Listo. Eliminé tus {count} gastos."
                        )

                elif result.action == "all_budgets_deleted":

                    count = result.data["count"]

                    if count == 1:
                        response_message = (
                            "🗑️ Listo. Eliminé tu presupuesto."
                        )
                    else:
                        response_message = (
                            f"🗑️ Listo. Eliminé tus {count} presupuestos."
                        )

                elif result.action == "pending_action_cancelled":

                    response_message = (
                        "👍 Operación cancelada."
                    )

                elif result.action == "pending_action_invalid_response":

                    response_message = (
                        result.data["message"]
                    )

                else:

                    response_message = (
                        result.data.get(
                            "message",
                            "No pude completar la operación.",
                        )
                    )

                # Guardar la respuesta en memoria
                AIMemoryService.add(
                    session_id=session_id,
                    role="user",
                    message=message,
                )

                AIMemoryService.add(
                    session_id=session_id,
                    role="assistant",
                    message=response_message,
                )

                return AIResponse(
                    success=result.success,
                    message=response_message,
                    data=result.data,
                )

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
            session_id=session_id,
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
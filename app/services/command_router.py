from sqlmodel import Session

from app.constants.intents import Intent
from app.schemas.ai_command import AICommand
from app.services.command_handlers import COMMAND_HANDLERS


class CommandRouter:

    @staticmethod
    def route(
        session: Session,
        command: AICommand,
        user_id: int | None = None,
        session_id: str | None = None,
    ):

        service = COMMAND_HANDLERS.get(command.intent)

        if service is None:
            return {
                "message": "Comando aún no implementado.",
                "intent": command.intent,
            }

        # ==========================================
        # SERVICIOS QUE NECESITAN SESSION_ID
        # ==========================================

        if command.intent in [
            Intent.DELETE_ALL_EXPENSES,
            Intent.DELETE_ALL_BUDGETS,
            Intent.UPDATE,
        ]:

            return service.process(
                session=session,
                command=command,
                user_id=user_id,
                session_id=session_id,
            )

        # ==========================================
        # SERVICIOS NORMALES
        # ==========================================

        return service.process(
            session=session,
            command=command,
            user_id=user_id,
        )
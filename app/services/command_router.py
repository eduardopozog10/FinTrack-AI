from sqlmodel import Session

from app.schemas.ai_command import AICommand
from app.services.command_handlers import COMMAND_HANDLERS


class CommandRouter:

    @staticmethod
    def route(
        session: Session,
        command: AICommand,
    ):

        service = COMMAND_HANDLERS.get(command.intent)

        if service is None:
            return {
                "message": "Comando aún no implementado.",
                "intent": command.intent,
            }

        return service.process(
            session=session,
            command=command,
        )
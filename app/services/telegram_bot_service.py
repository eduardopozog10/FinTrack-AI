from sqlmodel import Session

from app.services.ai_orchestrator import AIOrchestrator
from app.services.telegram_service import TelegramService
from app.services.telegram_user_service import TelegramUserService

class TelegramBotService:

    last_update_id: int | None = None

    @staticmethod
    def process_update(
        session: Session,
        update: dict,
    ):

        update_id = update.get("update_id")

        if update_id is not None:
            TelegramBotService.last_update_id = update_id

        message_data = update.get("message")

        if not message_data:
            return None

        text = message_data.get("text")
        chat = message_data.get("chat")
        user = message_data.get("from")

        if not text or not chat or not user:
            return None

        chat_id = chat.get("id")
        user_id = user.get("id")

        if chat_id is None or user_id is None:
            return None

        first_name = user.get("first_name", "")
        last_name = user.get("last_name", "")

        full_name = f"{first_name} {last_name}".strip()

        if not full_name:
            full_name = f"Telegram {user_id}"

        fintrack_user = TelegramUserService.get_or_create(
            session=session,
            telegram_id=user_id,
            full_name=full_name,
        )

        session_id = f"telegram_{user_id}"

        print("========== Telegram ==========")
        print("User ID:", user_id)
        print("Chat ID:", chat_id)
        print("Session ID:", session_id)
        print("Mensaje:", text)
        print("==============================")

        response = AIOrchestrator.process(
            session=session,
            message=text,
            session_id=session_id,
            user_id=fintrack_user.id,
            user_name=fintrack_user.full_name,
        )

        TelegramService.send_message(
            chat_id=chat_id,
            text=response.message,
        )

        return response
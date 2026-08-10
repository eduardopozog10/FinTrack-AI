import time

from sqlmodel import Session

from app.database.database import engine
from app.services.telegram_service import TelegramService
from app.services.telegram_bot_service import TelegramBotService


class TelegramPollingService:

    @staticmethod
    def run():

        print("===================================")
        print("🤖 Telegram polling iniciado")
        print("===================================")

        while True:

            try:
                offset = None

                if TelegramBotService.last_update_id is not None:
                    offset = TelegramBotService.last_update_id + 1

                updates_response = TelegramService.get_updates(
                    offset=offset,
                )

                updates = updates_response.get("result", [])

                for update in updates:

                    with Session(engine) as session:

                        TelegramBotService.process_update(
                            session=session,
                            update=update,
                        )

            except Exception as error:

                print("Error en Telegram polling:")
                print(error)

                time.sleep(3)
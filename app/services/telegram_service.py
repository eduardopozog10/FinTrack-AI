import requests

from app.core.config import settings


class TelegramService:

    BASE_URL = "https://api.telegram.org"

    @staticmethod
    def get_bot_info():

        url = (
            f"{TelegramService.BASE_URL}/bot"
            f"{settings.telegram_bot_token}/getMe"
        )

        response = requests.get(
            url,
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

    @staticmethod
    def get_updates(offset: int | None = None):

        url = (
            f"{TelegramService.BASE_URL}/bot"
            f"{settings.telegram_bot_token}/getUpdates"
        )

        params = {
            "timeout": 30,
        }

        if offset is not None:
            params["offset"] = offset

        response = requests.get(
            url,
            params=params,
            timeout=35,
        )

        response.raise_for_status()

        return response.json()

    @staticmethod
    def send_message(
        chat_id: int,
        text: str,
    ):

        url = (
            f"{TelegramService.BASE_URL}/bot"
            f"{settings.telegram_bot_token}/sendMessage"
        )

        payload = {
            "chat_id": chat_id,
            "text": text,
        }

        response = requests.post(
            url,
            json=payload,
            timeout=10,
        )

        response.raise_for_status()

        return response.json()
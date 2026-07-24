import re


class AmountExtractor:

    @staticmethod
    def extract(
        message: str,
    ):

        text = message.lower()

        # Eliminar símbolos
        text = text.replace("$", "")
        text = text.replace(".", "")
        text = text.replace(",", "")

        match = re.search(r"\d+", text)

        if not match:
            return None

        amount = int(match.group())

        # Ej: 15 lucas
        if "luca" in text:
            amount *= 1000

        # Ej: 15 mil
        elif "mil" in text and amount < 1000:
            amount *= 1000

        return amount
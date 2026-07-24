from app.constants.intents import Intent


class IntentClassifier:

    INCOME_PATTERNS = [
        "me pagaron",
        "recib",
        "deposit",
        "ingres",
        "gan",
        "cobr",
        "vend",
    ]

    EXPENSE_PATTERNS = [
        "gast",
        "compr",
        "pagué",
        "pague",
        "cost",
        "invert",
    ]

    BALANCE_PATTERNS = [
        "saldo",
        "cuánto tengo",
        "cuanto tengo",
        "dinero disponible",
    ]

    LIST_PATTERNS = [
        "mostrar",
         "muéstr",
        "listar",
         "lista",
        "ver",
         "historial",
        "movimientos",
        "transacciones",
    ]

    @staticmethod
    def detect(
        message: str,
    ):

        text = message.lower()

        if any(pattern in text for pattern in IntentClassifier.INCOME_PATTERNS):
            return Intent.INCOME

        if any(pattern in text for pattern in IntentClassifier.EXPENSE_PATTERNS):
            return Intent.EXPENSE

        if any(pattern in text for pattern in IntentClassifier.BALANCE_PATTERNS):
            return Intent.BALANCE

        if any(pattern in text for pattern in IntentClassifier.LIST_PATTERNS):
            return Intent.LIST


        return Intent.UNKNOWN
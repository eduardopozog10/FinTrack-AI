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

    UPDATE_PATTERNS = [
        "cambia",
        "cambiar",
        "corrige",
        "corregir",
        "actualiza",
        "actualizar",
        "modifica",
        "modificar",
    ]

    DELETE_PATTERNS = [
    "elimina",
    "eliminar",
    "borra",
    "borrar",
    "quita",
    "quitar",
    ]

    @staticmethod
    def detect(
        message: str,
    ):

        text = message.lower()

        if any(pattern in text for pattern in IntentClassifier.INCOME_PATTERNS):
            return Intent.INCOME

        if any(pattern in text for pattern in IntentClassifier.UPDATE_PATTERNS):
            return Intent.UPDATE

        if any(pattern in text for pattern in IntentClassifier.DELETE_PATTERNS):    
            return Intent.DELETE

        if any(pattern in text for pattern in IntentClassifier.EXPENSE_PATTERNS):
            return Intent.EXPENSE

        if any(pattern in text for pattern in IntentClassifier.BALANCE_PATTERNS):
            return Intent.BALANCE

        if any(pattern in text for pattern in IntentClassifier.LIST_PATTERNS):
            return Intent.LIST

        return Intent.UNKNOWN
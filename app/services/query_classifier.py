class QueryClassifier:

    TOTAL_EXPENSE_PATTERNS = [
        "cuánto gast",
        "cuanto gast",
        "total gast",
        "cuánto pag",
        "cuanto pag",
        "cuánto compr",
        "cuanto compr",
    ]

    TOTAL_INCOME_PATTERNS = [
        "cuánto gan",
        "cuanto gan",
        "cuánto ingres",
        "cuanto ingres",
        "cuánto recib",
        "cuanto recib",
        "cuánto cobr",
        "cuanto cobr",
    ]

    TODAY_EXPENSE_PATTERNS = [
        "gasté hoy",
        "gaste hoy",
        "hoy gast",
        "cuánto gasté hoy",
        "cuanto gaste hoy",
    ]

    MONTH_EXPENSE_PATTERNS = [
        "gasté este mes",
        "gaste este mes",
        "cuánto gasté este mes",
        "cuanto gaste este mes",
    ]

    MONTH_INCOME_PATTERNS = [
        "gané este mes",
        "gane este mes",
        "ingresé este mes",
        "ingrese este mes",
        "recibí este mes",
        "recibi este mes",
        "cuánto gané este mes",
        "cuanto gane este mes",
    ]

    MAX_EXPENSE_PATTERNS = [
    "mayor gasto",
    "gasto más alto",
    "gasto mas alto",
    "gasto más grande",
    "gasto mas grande",
    "compra más cara",
    "compra mas cara",
    "qué compré más caro",
    "que compre mas caro",
    ]

    MAX_INCOME_PATTERNS = [
    "mayor ingreso",
    "ingreso más alto",
    "ingreso mas alto",
    "ingreso más grande",
    "ingreso mas grande",
    "mayor sueldo",
    "sueldo más alto",
    "sueldo mas alto",
    "mayor depósito",
    "mayor deposito",
    "depósito más grande",
    "deposito mas grande",
    ]

    @staticmethod
    def detect(
        message: str,
    ):

        text = message.lower()

        if any(pattern in text for pattern in QueryClassifier.TODAY_EXPENSE_PATTERNS):
            return "TODAY_EXPENSE"

        if any(pattern in text for pattern in QueryClassifier.MONTH_INCOME_PATTERNS):
            return "MONTH_INCOME"

        if any(pattern in text for pattern in QueryClassifier.MONTH_EXPENSE_PATTERNS):
            return "MONTH_EXPENSE"

        if any(pattern in text for pattern in QueryClassifier.MAX_EXPENSE_PATTERNS):
            return "MAX_EXPENSE"

        if any(pattern in text for pattern in QueryClassifier.MAX_INCOME_PATTERNS):
            return "MAX_INCOME" 

        if any(pattern in text for pattern in QueryClassifier.TOTAL_INCOME_PATTERNS):
            return "TOTAL_INCOME"

        if any(pattern in text for pattern in QueryClassifier.TOTAL_EXPENSE_PATTERNS):
            return "TOTAL_EXPENSE"

        return None
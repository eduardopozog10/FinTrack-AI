class QueryClassifier:

    TOTAL_EXPENSE_PATTERNS = [
        "cuánto gast",
        "cuanto gast",
        "total gast",
        "cuánto pag",
        "cuanto pag",
        "cuánto compr",
        "cuanto compr",

        "cuánto he gastado",
        "cuanto he gastado",
        "he gastado",
        "llevo gastado",
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

        "cuánto he ganado",
        "cuanto he ganado",
        "he ganado",
        "llevo ganado",
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

    LAST_EXPENSE_PATTERNS = [
        "último gasto",
        "ultimo gasto",

        "mi último gasto",
        "mi ultimo gasto",

        "cuál fue mi último gasto",
        "cual fue mi ultimo gasto",

        "cuál fue el último gasto",
        "cual fue el ultimo gasto",
        "último pago",
        "ultimo pago",

        "qué compré recién",
        "que compré recién",
        "qué compre recién",
        "que compre recién",

        "qué compré recien",
        "que compré recien",
        "qué compre recien",
        "que compre recien",

        "qué pagué recién",
        "que pagué recién",
        "qué pague recién",
        "que pague recién",

        "qué pagué recien",
        "que pagué recien",
        "qué pague recien",
        "que pague recien",
    ]

    LAST_INCOME_PATTERNS = [
    "mi último ingreso",
    "mi ultimo ingreso",

    "cuál fue mi último ingreso",
    "cual fue mi ultimo ingreso",

    "cuál fue el último ingreso",
    "cual fue el ultimo ingreso",
    "último ingreso",
    "ultimo ingreso",

    "último sueldo",
    "ultimo sueldo",

    "último depósito",
    "ultimo deposito",

    "qué recibí recién",
    "que recibí recién",
    "qué recibi recién",
    "que recibi recién",

    "qué recibí recien",
    "que recibí recien",
    "qué recibi recien",
    "que recibi recien",

    "qué me pagaron",
    "que me pagaron",

    "qué depositaron",
    "que depositaron",

    "qué me depositaron",
    "que me depositaron",
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

        if any(pattern in text for pattern in QueryClassifier.LAST_EXPENSE_PATTERNS):
            return "LAST_EXPENSE"

        if any(pattern in text for pattern in QueryClassifier.LAST_INCOME_PATTERNS):
            return "LAST_INCOME"

        if any(pattern in text for pattern in QueryClassifier.TOTAL_INCOME_PATTERNS):
            return "TOTAL_INCOME"

        if any(pattern in text for pattern in QueryClassifier.TOTAL_EXPENSE_PATTERNS):
            return "TOTAL_EXPENSE"

        return None
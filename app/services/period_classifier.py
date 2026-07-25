class PeriodClassifier:

    TODAY_PATTERNS = [
        "hoy",
    ]

    MONTH_PATTERNS = [
        "este mes",
        "del mes",
        "mensual",
    ]

    YEAR_PATTERNS = [
        "este año",
        "del año",
        "anual",
    ]

    WEEK_PATTERNS = [
        "esta semana",
        "de la semana",
        "semanal",
    ]

    @staticmethod
    def detect(
        message: str,
    ):

        text = message.lower()

        if any(pattern in text for pattern in PeriodClassifier.TODAY_PATTERNS):
            return "TODAY"

        if any(pattern in text for pattern in PeriodClassifier.WEEK_PATTERNS):
            return "WEEK"

        if any(pattern in text for pattern in PeriodClassifier.MONTH_PATTERNS):
            return "MONTH"

        if any(pattern in text for pattern in PeriodClassifier.YEAR_PATTERNS):
            return "YEAR"

        return None
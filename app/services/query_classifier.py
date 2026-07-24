class QueryClassifier:

    @staticmethod
    def detect(
        message: str,
    ):

        text = message.lower()

        # Si no parece una pregunta, no es una consulta
        if not any(word in text for word in [
            "cuánto",
            "cuanto",
            "cuál",
            "cual",
            "total",
        ]):
            return None

        # Consulta de gastos
        if any(word in text for word in [
            "gast",
            "pag",
            "compr",
            "cost",
        ]):
            return "TOTAL_EXPENSE"

        # Consulta de ingresos
        if any(word in text for word in [
            "gan",
            "ingres",
            "recib",
            "cobr",
            "deposit",
        ]):
            return "TOTAL_INCOME"

        return None
class QueryClassifier:

    @staticmethod
    def detect(
        message: str,
    ):

        text = message.lower()

        if any(word in text for word in [
            "gasté",
            "gaste",
            "gasto",
        ]):
            return "TOTAL_EXPENSE"

        if any(word in text for word in [
            "gané",
            "gane",
            "ingresé",
            "ingrese",
            "recibí",
            "recibi",
        ]):
            return "TOTAL_INCOME"

        return None
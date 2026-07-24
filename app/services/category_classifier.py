from app.constants.categories import Category


class CategoryClassifier:

    @staticmethod
    def detect(
        message: str,
    ):

        text = message.lower()

        if any(word in text for word in [
            "supermercado",
            "lider",
            "jumbo",
            "unimarc",
            "santa isabel",
            "tottus",
        ]):
            return Category.SUPERMARKET

        if any(word in text for word in [
            "pizza",
            "hamburguesa",
            "comida",
            "almuerzo",
            "cena",
            "desayuno",
            "pan",
            "sushi",
            "restaurant",
        ]):
            return Category.FOOD

        if any(word in text for word in [
            "bencina",
            "copec",
            "shell",
            "petrobras",
            "uber",
            "taxi",
            "micro",
            "metro",
        ]):
            return Category.TRANSPORT

        if any(word in text for word in [
            "netflix",
            "spotify",
            "cine",
            "steam",
            "playstation",
            "xbox",
        ]):
            return Category.ENTERTAINMENT

        if any(word in text for word in [
            "doctor",
            "farmacia",
            "medicamento",
            "consulta",
        ]):
            return Category.HEALTH

        if any(word in text for word in [
            "curso",
            "universidad",
            "colegio",
            "libro",
        ]):
            return Category.EDUCATION

        if any(word in text for word in [
            "sueldo",
            "salario",
            "empresa",
        ]):
            return Category.SALARY

        return Category.OTHER
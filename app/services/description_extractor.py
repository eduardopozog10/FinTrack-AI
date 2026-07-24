import re

UPDATE_STOP_WORDS = [
    "el",
    "la",
    "los",
    "las",
    "un",
    "una",
    "unos",
    "unas",
    "del",
    "de",
    "al",
    "precio",
    "pago",
    "gasto",
    "compra",
    "valor",
    "monto",
    "costo",
    "importe",
    "transaccion",
    "transacción",
]

COMMON_VERBS = [
    "me compré",
    "me compre",
    "compré",
    "compre",
    "gasté",
    "gaste",
    "pagué",
    "pague",
    "aboné",
    "abone",
    "recibí",
    "recibi",
    "ingresé",
    "ingrese",
    "gané",
    "gane",
    "deposité",
    "deposite",
    "transferí",
    "transferi",
    "vendí",
    "vendi",
    "me pagaron",
    "me depositaron",
    "me transfirieron",
]

COMMON_CONNECTORS = [
    "por",
    "de",
    "del",
    "que fueron",
    "que fue",
    "que costó",
    "que costo",
    "costó",
    "costo",
]

COMMON_ARTICLES = [
    "el",
    "la",
    "los",
    "las",
    "un",
    "una",
    "unos",
    "unas",
    "mi",
    "mis",
]


class DescriptionExtractor:

    @staticmethod
    def _remove_verbs(text: str):

        for verb in sorted(COMMON_VERBS, key=len, reverse=True):
            if text.startswith(verb):
                text = text[len(verb):]
                break

        return text.strip()

    @staticmethod
    def _remove_amounts(text: str):

        text = re.sub(
            r"\$?[\d\.,]+",
            "",
            text,
        )

        text = re.sub(
            r"\b(mil|lucas?)\b",
            "",
            text,
        )

        return text

    @staticmethod
    def _remove_connectors(text: str):

        return re.sub(
            rf"\b({'|'.join(COMMON_CONNECTORS)})\b",
            "",
            text,
        )

    @staticmethod
    def _remove_articles(text: str):

        return re.sub(
            rf"\b({'|'.join(COMMON_ARTICLES)})\b",
            "",
            text,
        )

    @staticmethod
    def _clean_spaces(text: str):

        return re.sub(
            r"\s+",
            " ",
            text,
        ).strip()

    @staticmethod
    def extract(
        message: str,
    ):

        text = message.lower().strip()

        # ---------------------------------------------------
        # Casos de ingresos sin descripción
        # Ej:
        # "Me pagaron 50000"
        # "Me depositaron 100000"
        # ---------------------------------------------------

        if re.fullmatch(
            r"(me pagaron|me depositaron|me transfirieron)\s+\$?[\d\.,]+",
            text,
        ):
            return "Ingreso"

        # ---------------------------------------------------
        # Actualizar / Eliminar
        # ---------------------------------------------------

        match = re.search(
            r"(?:corrige|cambia|actualiza|modifica|borra|borrar|elimina|eliminar|quita|quitar)\s+(.+?)(?:\s+a\s+.+)?$",
            text,
        )

        if match:

            description = match.group(1)

            description = re.sub(
                rf"\b({'|'.join(UPDATE_STOP_WORDS)})\b",
                "",
                description,
            )

            description = DescriptionExtractor._clean_spaces(
                description,
            )

            return description.title()

        # ---------------------------------------------------
        # Buscar "en ..."
        # Ej: Gasté 15000 en Jumbo
        # ---------------------------------------------------

        match = re.search(
            r"\ben\s+(.+)",
            text,
        )

        if match:

            description = match.group(1)

            description = DescriptionExtractor._remove_amounts(
                description,
            )

            description = DescriptionExtractor._remove_connectors(
                description,
            )

            description = DescriptionExtractor._remove_articles(
                description,
            )

            description = DescriptionExtractor._clean_spaces(
                description,
            )

            return description.title()

        # ---------------------------------------------------
        # Buscar "para ..."
        # Ej: Compré regalo para mamá
        # ---------------------------------------------------

        match = re.search(
            r"\bpara\s+(.+)",
            text,
        )

        if match:

            description = match.group(1)

            description = DescriptionExtractor._remove_amounts(
                description,
            )

            description = DescriptionExtractor._remove_connectors(
                description,
            )

            description = DescriptionExtractor._remove_articles(
                description,
            )

            description = DescriptionExtractor._clean_spaces(
                description,
            )

            return description.title()

        # ---------------------------------------------------
        # Flujo general
        # ---------------------------------------------------

        text = DescriptionExtractor._remove_verbs(
            text,
        )

        text = DescriptionExtractor._remove_amounts(
            text,
        )

        text = DescriptionExtractor._remove_connectors(
            text,
        )

        text = DescriptionExtractor._remove_articles(
            text,
        )

        text = DescriptionExtractor._clean_spaces(
            text,
        )

        # Si quedó vacío, devolver una descripción genérica
        if not text:
            return "Ingreso"

        return text.title()
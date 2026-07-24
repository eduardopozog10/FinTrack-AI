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


class DescriptionExtractor:

    @staticmethod
    def extract(
        message: str,
    ):

        text = message.lower().strip()

        # ---------------------------------------------------
        # Actualizar / Eliminar
        # Ej:
        # "actualiza netflix a 15990"
        # "corrige el pago de netflix a 15990"
        # "borra netflix"
        # "elimina la compra del lider"
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

            description = re.sub(
                r"\s+",
                " ",
                description,
            ).strip()

            return description.title()

        # ---------------------------------------------------
        # Buscar "en ..."
        # Ej:
        # "gasté 15000 en jumbo"
        # ---------------------------------------------------

        match = re.search(
            r"\ben\s+(.+)",
            text,
        )

        if match:
            return match.group(1).strip().title()

        # ---------------------------------------------------
        # Buscar "para ..."
        # Ej:
        # "compré regalo para mamá"
        # ---------------------------------------------------

        match = re.search(
            r"\bpara\s+(.+)",
            text,
        )

        if match:
            return match.group(1).strip().title()

        # ---------------------------------------------------
        # Registrar gastos / ingresos
        # ---------------------------------------------------

        text = re.sub(
            r"^(gast[eé]|pagu[eé]|compr[eé]|abon[eé]|transfer[ií]|recib[ií]|gan[eé]|ingres[eé]|deposit[eé])\s+",
            "",
            text,
        )

        # Eliminar montos
        text = re.sub(
            r"\$?[\d\.,]+",
            "",
            text,
        )

        # Eliminar palabras comunes de montos
        text = re.sub(
            r"\b(mil|lucas?)\b",
            "",
            text,
        )

        # Limpiar espacios
        text = re.sub(
            r"\s+",
            " ",
            text,
        ).strip()

        return text.title()
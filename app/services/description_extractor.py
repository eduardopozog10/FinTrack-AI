import re


class DescriptionExtractor:

    @staticmethod
    def extract(
        message: str,
    ):

        text = message.lower()

        # Buscar "en ..."
        match = re.search(r"\ben\s+(.+)", text)

        if match:
            return match.group(1).strip().title()

        # Buscar "para ..."
        match = re.search(r"\bpara\s+(.+)", text)

        if match:
            return match.group(1).strip().title()

        # Eliminar verbos comunes
        text = re.sub(
            r"^(gast[eé]|pagu[eé]|compr[eé]|abon[eé]|transfer[ií])\s+",
            "",
            text,
        )

        # Eliminar el monto
        text = re.sub(r"\$?[\d\.,]+", "", text)

        # Eliminar "mil" o "lucas"
        text = re.sub(r"\b(mil|lucas?)\b", "", text)

        # Limpiar espacios
        text = re.sub(r"\s+", " ", text).strip()

        return text.title()
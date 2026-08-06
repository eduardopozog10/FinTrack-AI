import unicodedata


class CategoryNormalizerService:

    CATEGORY_MAP = {

        # ==========================
        # COMIDA
        # ==========================

        "comida": "comida",
        "supermercado": "comida",
        "mercado": "comida",
        "almuerzo": "comida",
        "desayuno": "comida",
        "cena": "comida",
        "restaurante": "comida",
        "delivery": "comida",
        "uber eats": "comida",
        "rappi": "comida",
        "cafetería": "comida",
        "café": "comida",
        "panadería": "comida",

        # ==========================
        # TRANSPORTE
        # ==========================

        "transporte": "transporte",
        "uber": "transporte",
        "cabify": "transporte",
        "taxi": "transporte",
        "metro": "transporte",
        "bus": "transporte",
        "bencina": "transporte",
        "combustible": "transporte",
        "peaje": "transporte",
        "estacionamiento": "transporte",

        # ==========================
        # HOGAR
        # ==========================

        "hogar": "hogar",
        "luz": "hogar",
        "agua": "hogar",
        "gas": "hogar",
        "internet": "hogar",

        # ==========================
        # OCIO
        # ==========================

        "ocio": "ocio",
        "cine": "ocio",
        "netflix": "ocio",
        "spotify": "ocio",
        "juegos": "ocio",

        # ==========================
        # SALUD
        # ==========================

        "salud": "salud",
        "farmacia": "salud",
        "medicamentos": "salud",
        "doctor": "salud",
    }

    @classmethod
    def normalize(
        cls,
        category: str | None,
    ) -> str | None:

        if category is None:
            return None

        category = (
            unicodedata.normalize("NFD", category)
            .encode("ascii", "ignore")
            .decode("utf-8")
            .lower()
            .strip()
        )

        normalized_map = {
            (
                unicodedata.normalize("NFD", key)
                .encode("ascii", "ignore")
                .decode("utf-8")
                .lower()
            ): value
            for key, value in cls.CATEGORY_MAP.items()
        }

        return normalized_map.get(
            category,
            category,
        )
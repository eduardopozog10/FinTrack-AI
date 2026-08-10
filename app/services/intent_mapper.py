class IntentMapper:

    INTENT_MAP = {
        "registrar_gasto": "add_transaction",
        "registrar_ingreso": "add_transaction",
        "consultar_balance": "get_balance",
        "consultar_gastos": "get_expenses",
        "consultar_ingresos": "get_income",
        "consultar_categoria": "get_category_expenses",
        "consultar_presupuesto": "get_budget",
    }

    @classmethod
    def map(cls, intent: str) -> str | None:
        return cls.INTENT_MAP.get(intent)
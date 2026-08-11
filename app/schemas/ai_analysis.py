from pydantic import BaseModel


class AITransactionItem(BaseModel):
    tipo_transaccion: str
    monto: float
    categoria_probable: str | None = None
    descripcion: str | None = None
    fecha_mencionada: str | None = None


class AIAnalysis(BaseModel):
    intencion_usuario: str
    backend_action: str | None = None
    query_type: str | None = None
    tipo_transaccion: str | None = None
    monto: float | None = None
    categoria_probable: str | None = None
    descripcion: str | None = None
    fecha_mencionada: str | None = None
    campo_actualizar: str | None = None
    nuevo_valor: str | float | None = None
    referencia_transaccion: str | None = None

    transacciones: list[AITransactionItem] | None = None
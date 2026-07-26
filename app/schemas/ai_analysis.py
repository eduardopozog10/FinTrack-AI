from pydantic import BaseModel


class AIAnalysis(BaseModel):
    intencion_usuario: str
    backend_action: str | None = None
    query_type: str | None = None
    tipo_transaccion: str | None = None
    monto: float | None = None
    categoria_probable: str | None = None
    descripcion: str | None = None
    fecha_mencionada: str | None = None
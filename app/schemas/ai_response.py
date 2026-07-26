from typing import Optional

from pydantic import BaseModel


class AIResponse(BaseModel):
    intencion_usuario: str
    tipo_transaccion: Optional[str] = None
    monto: Optional[float] = None
    categoria_probable: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_mencionada: Optional[str] = None
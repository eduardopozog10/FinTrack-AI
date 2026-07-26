from typing import Any

from pydantic import BaseModel


class AIResponse(BaseModel):

    success: bool

    message: str

    data: Any | None = None
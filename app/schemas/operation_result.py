from typing import Any

from pydantic import BaseModel


class OperationResult(BaseModel):

    success: bool

    action: str

    data: Any = None

    metadata: dict[str, Any] | None = None
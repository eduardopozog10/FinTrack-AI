from typing import Any

from pydantic import BaseModel


class ConversationContext(BaseModel):

    action: str

    success: bool

    user_message: str

    data: Any

    metadata: dict[str, Any] | None = None
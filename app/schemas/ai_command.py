from pydantic import BaseModel

from app.schemas.query_filter import QueryFilter


class AICommand(BaseModel):

    intent: str

    query_filter: QueryFilter | None = None

    amount: float | None = None

    category: str | None = None

    description: str | None = None
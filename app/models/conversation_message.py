from datetime import datetime

from sqlmodel import Field, SQLModel


class ConversationMessage(SQLModel, table=True):

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    session_id: str

    role: str

    message: str

    created_at: datetime = Field(
        default_factory=datetime.now,
    )
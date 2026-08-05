from datetime import datetime

from sqlmodel import Field, SQLModel


class Budget(SQLModel, table=True):

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    category: str = Field(
        index=True,
    )

    amount: float

    created_at: datetime = Field(
        default_factory=datetime.now,
    )
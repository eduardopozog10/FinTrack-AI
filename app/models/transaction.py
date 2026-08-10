from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from app.constants.transaction_type import TransactionType


class Transaction(SQLModel, table=True):

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )

    user_id: Optional[int] = Field(
        default=None,
        foreign_key="user.id",
        index=True,
    )

    description: str

    amount: float

    transaction_type: TransactionType

    category: str

    created_at: datetime = Field(
        default_factory=datetime.now,
    )
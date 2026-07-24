from datetime import datetime
from app.constants.transaction_type import TransactionType
from typing import Optional
from sqlmodel import Field, SQLModel


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    description: str

    amount: float

    transaction_type: TransactionType

    category: str

    created_at: datetime = Field(default_factory=datetime.now)
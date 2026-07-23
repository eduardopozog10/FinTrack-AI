from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class TransactionType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    description: str

    amount: float

    transaction_type: TransactionType

    category: str

    created_at: datetime = Field(default_factory=datetime.now)
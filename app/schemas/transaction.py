from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel

from app.models.transaction import TransactionType


class TransactionCreate(SQLModel):
    description: str
    amount: float
    transaction_type: TransactionType
    category: str


class TransactionRead(SQLModel):
    id: int
    description: str
    amount: float
    transaction_type: TransactionType
    category: str
    created_at: datetime


class TransactionUpdate(SQLModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    transaction_type: Optional[TransactionType] = None
    category: Optional[str] = None
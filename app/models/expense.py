from typing import Optional

from sqlmodel import Field, SQLModel


class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    description: str
    amount: float
    category: str
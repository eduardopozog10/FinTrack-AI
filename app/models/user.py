from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )

    full_name: str

    email: str = Field(
        unique=True,
        index=True,
    )

    hashed_password: str
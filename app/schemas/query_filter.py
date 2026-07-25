from dataclasses import dataclass
from typing import Optional

from app.constants.transaction_type import TransactionType


@dataclass
class QueryFilter:

    action: str

    transaction_type: Optional[TransactionType] = None

    category: Optional[str] = None

    period: Optional[str] = None
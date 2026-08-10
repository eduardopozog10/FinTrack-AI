from dataclasses import dataclass

from app.models.transaction import Transaction


@dataclass
class TransactionUpdatedEvent:

    transaction: Transaction

    previous_category: str | None

    previous_amount: float | None

    metadata: dict | None = None
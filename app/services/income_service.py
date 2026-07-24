from sqlmodel import Session

from app.models.transaction import TransactionType
from app.services.transaction_service import TransactionService


class IncomeService:

    @staticmethod
    def process(
        session: Session,
        amount: float,
        category: str,
        description: str,
    ):

        return TransactionService.create_from_message(
            session=session,
            amount=amount,
            category=category,
            description=description,
            transaction_type=TransactionType.INCOME,
        )
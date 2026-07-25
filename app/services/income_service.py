from sqlmodel import Session

from app.constants.categories import Category
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

        if category is None:
            category = Category.OTHER

        if not description:
            description = "Ingreso"

        return TransactionService.create_from_message(
            session=session,
            amount=amount,
            category=category,
            description=description,
            transaction_type=TransactionType.INCOME,
        )
from sqlmodel import Session, select
from sqlalchemy import func

from app.models.transaction import Transaction


class QueryService:

    @staticmethod
    def process(
        session: Session,
        category: str | None = None,
        transaction_type: str | None = None,
    ):

        query = select(func.sum(Transaction.amount))

        if category:
            query = query.where(
                Transaction.category == category
            )

        if transaction_type:
            query = query.where(
                Transaction.transaction_type == transaction_type
            )

        total = session.exec(query).one()

        return {
            "total": total or 0,
            "category": category,
            "transaction_type": transaction_type,
        }
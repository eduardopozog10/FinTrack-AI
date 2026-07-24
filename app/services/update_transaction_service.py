from sqlmodel import Session, select

from app.models.transaction import Transaction


class UpdateTransactionService:

    @staticmethod
    def process(
        session: Session,
        description: str,
        amount: float,
    ):

        print("Descripción a buscar:", description)

        transaction = session.exec(
            select(Transaction)
            .where(
                Transaction.description.ilike(f"%{description}%")
            )
            .order_by(
                Transaction.created_at.desc(),
            )
        ).first()

        if transaction is None:
            return {
                "message": "No encontré esa transacción.",
            }

        transaction.amount = amount

        session.add(transaction)
        session.commit()
        session.refresh(transaction)

        return transaction
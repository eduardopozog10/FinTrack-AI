from sqlmodel import Session, select

from app.models.transaction import Transaction


class DeleteTransactionService:

    @staticmethod
    def process(
        session: Session,
        description: str,
    ):

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

        session.delete(transaction)
        session.commit()

        return {
            "message": "Transacción eliminada correctamente.",
            "description": transaction.description,
        }
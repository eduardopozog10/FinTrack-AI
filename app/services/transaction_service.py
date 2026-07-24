from sqlmodel import Session, select

from app.models.transaction import (
    Transaction,
    TransactionType,
)
from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
)


class TransactionService:

    @staticmethod
    def create(session: Session, transaction: TransactionCreate):
        db_transaction = Transaction(**transaction.model_dump())

        session.add(db_transaction)
        session.commit()
        session.refresh(db_transaction)

        return db_transaction

    @staticmethod
    def create_from_message(
        session: Session,
        amount: float,
        category: str,
        description: str,
        transaction_type: TransactionType,
    ):

        db_transaction = Transaction(
            description=description,
            amount=amount,
            transaction_type=transaction_type,
            category=category,
        )

        session.add(db_transaction)
        session.commit()
        session.refresh(db_transaction)

        return db_transaction


    @staticmethod
    def get_all(session: Session):
        statement = select(Transaction)
        return session.exec(statement).all()

    @staticmethod
    def get_by_id(session: Session, transaction_id: int):
        return session.get(Transaction, transaction_id)

    @staticmethod
    def update(
        session: Session,
        db_transaction: Transaction,
        transaction: TransactionUpdate,
    ):

        data = transaction.model_dump(exclude_unset=True)

        for key, value in data.items():
            setattr(db_transaction, key, value)

        session.add(db_transaction)
        session.commit()
        session.refresh(db_transaction)

        return db_transaction

    @staticmethod
    def delete(
        session: Session,
        db_transaction: Transaction,
    ):
        session.delete(db_transaction)
        session.commit()
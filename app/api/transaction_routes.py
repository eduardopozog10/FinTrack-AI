from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database.database import get_session
from app.schemas.transaction import (
    TransactionCreate,
    TransactionRead,
    TransactionUpdate,
)
from app.services.transaction_service import TransactionService

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@router.post("/", response_model=TransactionRead)
def create_transaction(
    transaction: TransactionCreate,
    session: Session = Depends(get_session),
):
    return TransactionService.create(session, transaction)


@router.get("/", response_model=list[TransactionRead])
def get_transactions(
    session: Session = Depends(get_session),
):
    return TransactionService.get_all(session)


@router.get("/{transaction_id}", response_model=TransactionRead)
def get_transaction(
    transaction_id: int,
    session: Session = Depends(get_session),
):
    transaction = TransactionService.get_by_id(
        session,
        transaction_id,
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found",
        )

    return transaction


@router.put("/{transaction_id}", response_model=TransactionRead)
def update_transaction(
    transaction_id: int,
    transaction: TransactionUpdate,
    session: Session = Depends(get_session),
):
    db_transaction = TransactionService.get_by_id(
        session,
        transaction_id,
    )

    if not db_transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found",
        )

    return TransactionService.update(
        session,
        db_transaction,
        transaction,
    )


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    session: Session = Depends(get_session),
):
    transaction = TransactionService.get_by_id(
        session,
        transaction_id,
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found",
        )

    TransactionService.delete(
        session,
        transaction,
    )

    return {
        "message": "Transaction deleted successfully"
    }
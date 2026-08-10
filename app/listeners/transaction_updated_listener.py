from app.constants.transaction_type import TransactionType
from app.services.budget_status_service import BudgetStatusService


class TransactionUpdatedListener:

    @staticmethod
    def handle(event):

        transaction = event.transaction

        # Los presupuestos solo nos interesan para gastos.
        if transaction.transaction_type != TransactionType.EXPENSE:
            return

        session = event.metadata.get("session")

        if session is None:
            return

        # Estado del presupuesto correspondiente
        # a la categoría actual de la transacción.
        budget_status = BudgetStatusService.get_status(
            session=session,
            category=transaction.category,
            user_id=transaction.user_id,
        )

        if budget_status is not None:
            event.metadata["budget"] = budget_status
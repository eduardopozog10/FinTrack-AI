from app.services.budget_status_service import BudgetStatusService


class BudgetListener:

    @staticmethod
    def handle(event):

        transaction = event.transaction

        status = BudgetStatusService.get_status(
            session=event.metadata["session"],
            category=transaction.category,
        )

        if status is not None:
            event.metadata["budget"] = status
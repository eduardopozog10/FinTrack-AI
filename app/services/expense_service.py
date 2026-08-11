from sqlmodel import Session

from app.constants.categories import Category
from app.models.transaction import TransactionType
from app.schemas.ai_command import AICommand
from app.schemas.operation_result import OperationResult
from app.services.transaction_service import TransactionService
from app.services.category_normalizer_service import CategoryNormalizerService
from app.events.event_bus import EventBus
from app.events.expense_created_event import ExpenseCreatedEvent


class ExpenseService:

    @staticmethod
    def process(
        session: Session,
        command: AICommand,
        user_id: int | None = None,
    ):

        # ==========================================
        # MÚLTIPLES GASTOS
        # ==========================================

        if command.transactions:

            created_transactions = []

            for item in command.transactions:

                # Solo procesamos gastos aquí
                if item.tipo_transaccion != "gasto":
                    continue

                category = CategoryNormalizerService.normalize(
                    item.categoria_probable
                )

                if category is None:
                    category = Category.OTHER

                description = item.descripcion

                if not description:
                    description = category.capitalize()

                transaction = TransactionService.create_from_message(
                    session=session,
                    amount=item.monto,
                    category=category,
                    description=description,
                    transaction_type=TransactionType.EXPENSE,
                    user_id=user_id,
                )

                metadata = {
                    "session": session,
                }

                event = ExpenseCreatedEvent(
                    transaction=transaction,
                    metadata=metadata,
                )

                EventBus.dispatch(event)

                created_transactions.append(transaction)

            return OperationResult(
                success=True,
                action="expenses_created",
                data=created_transactions,
            )

        # ==========================================
        # GASTO INDIVIDUAL
        # ==========================================

        amount = command.amount

        category = CategoryNormalizerService.normalize(
            command.category
        )

        description = command.description

        if category is None:
            category = Category.OTHER

        if not description:
            description = category.capitalize()

        transaction = TransactionService.create_from_message(
            session=session,
            amount=amount,
            category=category,
            description=description,
            transaction_type=TransactionType.EXPENSE,
            user_id=user_id,
        )

        metadata = {
            "session": session,
        }

        event = ExpenseCreatedEvent(
            transaction=transaction,
            metadata=metadata,
        )

        EventBus.dispatch(event)

        return OperationResult(
            success=True,
            action="expense_created",
            data=transaction,
            metadata=event.metadata,
        )
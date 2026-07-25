from sqlmodel import Session

from app.constants.intents import Intent
from app.constants.transaction_type import TransactionType

from app.services.amount_extractor import AmountExtractor
from app.services.category_classifier import CategoryClassifier
from app.services.command_router import CommandRouter
from app.services.description_extractor import DescriptionExtractor
from app.services.intent_classifier import IntentClassifier
from app.services.query_classifier import QueryClassifier
from app.services.period_classifier import PeriodClassifier
from app.services.transaction_filter_builder import TransactionFilterBuilder

class MessageService:

    @staticmethod
    def process_message(
        session: Session,
        message: str,
    ):

        amount = AmountExtractor.extract(
            message,
        )

        category = CategoryClassifier.detect(
            message,
        )

        description = DescriptionExtractor.extract(
            message,
        )

        intent = IntentClassifier.detect(
            message,
        )

        query_type = QueryClassifier.detect(
            message,
        )

        period = PeriodClassifier.detect(
            message,
        )

        if query_type:
            intent = Intent.QUERY

        transaction_type = None

        if query_type:

            if "EXPENSE" in query_type:
                transaction_type = TransactionType.EXPENSE

            elif "INCOME" in query_type:
                transaction_type = TransactionType.INCOME

        query_filter = None

        if query_type:

            query_filter = TransactionFilterBuilder.build(
                query_type=query_type,
                transaction_type=transaction_type,
                category=category,
                period=period,
            )

        print("Mensaje:", message)
        print("Intent:", intent)
        print("Query:", query_type)
        print("Periodo:", period)
        print("Descripción:", description)
        print("Monto:", amount)
        print("QueryFilter:", query_filter)

        return CommandRouter.route(
            session=session,
            intent=intent,
            query_filter=query_filter,
            amount=amount,
            category=category,
            description=description,
        )
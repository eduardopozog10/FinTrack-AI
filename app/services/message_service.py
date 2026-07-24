from sqlmodel import Session

from app.constants.intents import Intent
from app.services.amount_extractor import AmountExtractor
from app.services.category_classifier import CategoryClassifier
from app.services.command_router import CommandRouter
from app.services.description_extractor import DescriptionExtractor
from app.services.intent_classifier import IntentClassifier
from app.services.query_classifier import QueryClassifier

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

        if query_type:
            intent = Intent.QUERY

        print("Mensaje:", message)
        print("Intent:", intent)
        print("Query:", query_type)
        print("Descripción:", description)

        return CommandRouter.route(
            session=session,
            intent=intent,
            query_type=query_type,
            amount=amount,
            category=category,
            description=description,
        )
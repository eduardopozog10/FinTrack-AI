from sqlmodel import Session, select

from app.models.conversation_message import ConversationMessage


class ConversationMessageRepository:

    @staticmethod
    def add(
        session: Session,
        session_id: str,
        role: str,
        message: str,
    ):

        conversation = ConversationMessage(
            session_id=session_id,
            role=role,
            message=message,
        )

        session.add(conversation)
        session.commit()

        return conversation


    @staticmethod
    def get_last_messages(
        session: Session,
        session_id: str,
        limit: int = 10,
    ):

        messages = session.exec(
            select(ConversationMessage)
            .where(
                ConversationMessage.session_id == session_id
            )
            .order_by(
                ConversationMessage.created_at.desc()
            )
            .limit(limit)
        ).all()

        messages.reverse()

        return messages


    @staticmethod
    def clear(
        session: Session,
        session_id: str,
    ):

        messages = session.exec(
            select(ConversationMessage)
            .where(
                ConversationMessage.session_id == session_id
            )
        ).all()

        for message in messages:
            session.delete(message)

        session.commit()
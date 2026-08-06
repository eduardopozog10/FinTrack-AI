from pydantic import BaseModel


class ExpenseCreatedEvent(BaseModel):

    transaction: object

    metadata: dict | None = None
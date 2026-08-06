from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.database.database import create_db_and_tables
from app.events.event_bus import EventBus
from app.events.expense_created_event import ExpenseCreatedEvent
from app.listeners.budget_listener import BudgetListener

app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.version,
)


@app.on_event("startup")
def on_startup():

    create_db_and_tables()

    EventBus.subscribe(
        ExpenseCreatedEvent,
        BudgetListener,
    )


app.include_router(router)
from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.database.database import create_db_and_tables
from app.events.event_bus import EventBus
from app.events.expense_created_event import ExpenseCreatedEvent
from app.listeners.budget_listener import BudgetListener
from app.events.transaction_updated_event import TransactionUpdatedEvent
from app.listeners.transaction_updated_listener import TransactionUpdatedListener
from app.listeners.budget_alert_listener import BudgetAlertListener
import threading

from app.services.telegram_polling_service import TelegramPollingService

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

    EventBus.subscribe(
        ExpenseCreatedEvent,
        BudgetAlertListener,
    )

    EventBus.subscribe(
        TransactionUpdatedEvent,
        TransactionUpdatedListener,
    )

    telegram_thread = threading.Thread(
        target=TelegramPollingService.run,
        daemon=True,
    )

    telegram_thread.start()


app.include_router(router)
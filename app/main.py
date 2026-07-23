from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.database.database import create_db_and_tables


app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.version,
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(router)
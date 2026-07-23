from fastapi import APIRouter

from app.api.transaction_routes import router as transaction_router
from app.api.message_routes import router as message_router

router = APIRouter()

router.include_router(message_router)
router.include_router(transaction_router)
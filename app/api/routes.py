from fastapi import APIRouter

from app.api.transaction_routes import router as transaction_router
from app.api.message_routes import router as message_router
from app.auth.auth_routes import router as auth_router

router = APIRouter()

router.include_router(message_router)
router.include_router(transaction_router)
router.include_router(auth_router)
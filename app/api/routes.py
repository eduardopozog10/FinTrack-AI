from fastapi import APIRouter

from app.schemas.message import MessageRequest
from app.core.config import settings

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": f"Welcome to {settings.app_name}!"
    }


@router.post("/messages")
def receive_message(request: MessageRequest):
    return {
        "status": "received",
        "message": request.message
    }
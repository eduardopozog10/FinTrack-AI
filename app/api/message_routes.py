from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.database import get_session
from app.services.message_service import MessageService
from fastapi import APIRouter
from app.core.config import settings
from app.schemas.message import MessageRequest

router = APIRouter(tags=["Messages"])


@router.get("/")
def root():
    return {
        "message": f"Welcome to {settings.app_name}!"
    }


@router.post("/messages")
def receive_message(
    request: MessageRequest,
    session: Session = Depends(get_session),
):

    return MessageService.process_message(
        session=session,
        message=request.message,
    )
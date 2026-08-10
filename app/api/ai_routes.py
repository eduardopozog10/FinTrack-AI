from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.schemas.ai_command import AICommand
from app.schemas.ai_request import AIRequest
from app.services.ai_orchestrator import AIOrchestrator
from app.services.telegram_service import TelegramService
from app.database.database import get_session
from app.services.telegram_bot_service import TelegramBotService


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post("/analyze")
def analyze_message(
    request: AIRequest,
    session: Session = Depends(get_session),
):

    return AIOrchestrator.process(
        session=session,
        message=request.message,
        session_id=request.session_id,
    )


@router.get("/telegram/test")
def test_telegram():

    return TelegramService.get_bot_info()

@router.get("/telegram/updates")
def telegram_updates():

    return TelegramService.get_updates()

@router.post("/telegram/send-test")
def telegram_send_test(
    chat_id: int,
):

    return TelegramService.send_message(
        chat_id=chat_id,
        text="Hola desde FinTrack 🚀",
    )

@router.post("/telegram/process")
def telegram_process(
    session: Session = Depends(get_session),
):

    offset = None

    if TelegramBotService.last_update_id is not None:
        offset = TelegramBotService.last_update_id + 1

    updates_response = TelegramService.get_updates(
        offset=offset,
    )

    updates = updates_response.get("result", [])

    processed = []

    for update in updates:

        result = TelegramBotService.process_update(
            session=session,
            update=update,
        )

        if result is not None:
            processed.append(result)

    return {
        "processed": len(processed),
        "last_update_id": TelegramBotService.last_update_id,
    }
from fastapi import APIRouter, Depends

from app.schemas.ai_command import AICommand
from app.schemas.ai_request import AIRequest
from app.services.ai_orchestrator import AIOrchestrator
from sqlmodel import Session

from app.database.database import get_session


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
    )
from fastapi import APIRouter

from app.schemas.ai_analysis import AIAnalysis
from app.schemas.ai_request import AIRequest
from app.services.ai_orchestrator import AIOrchestrator


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post("/analyze", response_model=AIAnalysis)
def analyze_message(request: AIRequest) -> AIAnalysis:

    return AIOrchestrator.process(
        request.message
    )
from app.schemas.ai_analysis import AIAnalysis
from app.services.gemini_service import GeminiService


class AIOrchestrator:

    @staticmethod
    def process(message: str) -> AIAnalysis:

        analysis = GeminiService.analyze_message(message)

        return analysis
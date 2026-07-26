import json

from google import genai

from app.core.config import settings
from app.schemas.ai_analysis import AIAnalysis
from app.services.intent_mapper import IntentMapper


class GeminiService:

    client = genai.Client(
        api_key=settings.gemini_api_key,
    )

    @staticmethod
    def analyze_message(message: str) -> AIAnalysis:

        prompt = f"""
Eres un asistente especializado en interpretar mensajes financieros.

Analiza el siguiente mensaje del usuario.

Mensaje:
{message}

Extrae la siguiente información:

- intencion_usuario
- tipo_transaccion: ingreso, gasto o null
- monto
- categoria_probable
- descripcion
- fecha_mencionada

Utiliza exclusivamente estas intenciones:

- registrar_gasto
- registrar_ingreso
- consultar_balance
- consultar_gastos
- consultar_ingresos
- consultar_categoria
- desconocida

Si un dato no está presente, utiliza null.

IMPORTANTE:
- Responde únicamente con un JSON válido.
- No escribas explicaciones.
- No escribas texto antes o después del JSON.
- No uses bloques ```json.

Formato esperado:

{{
    "intencion_usuario": "registrar_gasto",
    "tipo_transaccion": "gasto",
    "monto": 12500,
    "categoria_probable": "cafetería",
    "descripcion": "Starbucks",
    "fecha_mencionada": "ayer"
}}
"""

        response = GeminiService.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )

        if not response.text:
            raise ValueError("Gemini no devolvió ninguna respuesta.")

        try:
            data = json.loads(response.text)

        except json.JSONDecodeError as error:
            raise ValueError(
                "Gemini devolvió una respuesta que no es un JSON válido."
            ) from error

        intent = data.get("intencion_usuario")

        if not intent:
            raise ValueError(
                "Gemini no devolvió la intención del usuario."
            )

        data["backend_action"] = IntentMapper.map(intent)

        return AIAnalysis.model_validate(data)
import json

from google import genai

from app.core.config import settings
from app.schemas.ai_analysis import AIAnalysis
from app.schemas.conversation_context import ConversationContext
from app.services.intent_mapper import IntentMapper


class GeminiService:

    client = genai.Client(
        api_key=settings.gemini_api_key,
    )

    @staticmethod
    def analyze_message(message: str) -> AIAnalysis:

        prompt = f"""
Eres un asistente especializado en interpretar mensajes financieros de una aplicación de control de gastos personales.

Tu única tarea es analizar el mensaje del usuario y devolver un JSON válido con la información extraída.

Mensaje del usuario:
{message}

========================
INTENCIONES DISPONIBLES
========================

Debes utilizar EXCLUSIVAMENTE una de estas intenciones:

- registrar_gasto
    El usuario quiere registrar un gasto.

- registrar_ingreso
    El usuario quiere registrar un ingreso.

- consultar_balance
    El usuario quiere conocer su saldo o balance.

- consultar_gastos
    El usuario quiere consultar uno o más gastos.

- consultar_ingresos
    El usuario quiere consultar uno o más ingresos.

- consultar_categoria
    El usuario quiere consultar gastos de una categoría específica.

- desconocida
    Cuando no sea posible identificar la intención.

========================
QUERY_TYPE
========================

Si la intención NO corresponde a una consulta, utiliza:

null

Si la intención corresponde a una consulta, utiliza EXCLUSIVAMENTE uno de los siguientes valores:

TODAY_EXPENSE
    Ejemplos:
    - ¿Cuánto gasté hoy?
    - Gastos de hoy

MONTH_EXPENSE
    Ejemplos:
    - ¿Cuánto gasté este mes?
    - Gastos del mes

MONTH_INCOME
    Ejemplos:
    - ¿Cuánto gané este mes?
    - Ingresos del mes

MAX_EXPENSE
    Ejemplos:
    - ¿Cuál fue mi gasto más grande?
    - Mayor gasto

MAX_INCOME
    Ejemplos:
    - ¿Cuál fue mi ingreso más grande?
    - Mayor ingreso

LAST_EXPENSE
    Ejemplos:
    - ¿Cuál fue mi último gasto?
    - Último gasto

LAST_INCOME
    Ejemplos:
    - ¿Cuál fue mi último ingreso?
    - Último ingreso

TOTAL_EXPENSE
    Ejemplos:
    - ¿Cuánto he gastado en total?
    - Total gastado

TOTAL_INCOME
    Ejemplos:
    - ¿Cuánto he ganado en total?
    - Total de ingresos

========================
TIPO DE TRANSACCIÓN
========================

Utiliza únicamente:

- gasto
- ingreso
- null

Si la intención no registra ni consulta una transacción específica, utiliza null.

========================
MONTO
========================

Extrae únicamente el valor numérico.

Ejemplos:

"Gasté $12.500"
→ 12500

"Recibí 350000 pesos"
→ 350000

Si no existe monto:

null

========================
CATEGORÍA
========================

Detecta la categoría más probable.

Ejemplos:

Starbucks → cafetería

Uber → transporte

Copec → combustible

Supermercado → supermercado

McDonald's → comida

Si no puede determinarse:

null

========================
DESCRIPCIÓN
========================

Extrae una descripción corta de la transacción.

Ejemplos:

"Gasté 5000 en Starbucks"

→ "Starbucks"

"Compré pan"

→ "pan"

Si no existe:

null

========================
FECHA
========================

Extrae únicamente la referencia temporal mencionada por el usuario.

Ejemplos:

"hoy"

"ayer"

"este mes"

"la semana pasada"

"enero"

Si el usuario no menciona una fecha:

null

========================
REGLAS GENERALES
========================

- Nunca inventes información que no esté presente en el mensaje.
- Si un dato no puede determinarse con seguridad, utiliza null.
- El monto siempre debe ser un número sin símbolos de moneda.
- La descripción debe ser breve.
- La categoría debe ser la más probable según el contexto.
- El query_type solo debe tener un valor cuando la intención sea una consulta.
- Si existen varias interpretaciones posibles, elige la más probable según el contexto del mensaje.

========================
FORMATO DE RESPUESTA
========================

Responde únicamente con un JSON válido.

No agregues explicaciones.

No escribas texto adicional.

No uses bloques ```json.

Debes responder exactamente con esta estructura:

{{
    "intencion_usuario": "registrar_gasto",
    "query_type": null,
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
            raise ValueError(
                "Gemini no devolvió ninguna respuesta."
            )

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

    @staticmethod
    def generate_response(
        context: ConversationContext,
    ) -> str:

        prompt = f"""
Eres FinTrack AI.

Tu trabajo consiste únicamente en comunicar al usuario el resultado que entregó el backend.

No tomas decisiones.

No ejecutas lógica de negocio.

No inventas información.

Nunca cambies montos.

Nunca cambies categorías.

Nunca digas que una operación fue exitosa si success es False.

Responde de forma breve, natural y cercana.

==========================
MENSAJE ORIGINAL
==========================

{context.user_message}

==========================
RESULTADO DEL BACKEND
==========================

Acción:
{context.action}

Éxito:
{context.success}

Datos:
{context.data}

==========================
REGLAS
==========================

- Usa únicamente la información proporcionada.
- No inventes datos.
- No expliques procesos internos.
- Responde en español.
- Devuelve únicamente el mensaje para el usuario.
"""

        response = GeminiService.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )

        if not response.text:
            raise ValueError(
                "Gemini no devolvió ninguna respuesta."
            )

        return response.text.strip()
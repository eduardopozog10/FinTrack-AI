import json
import time

from google import genai

from app.core.config import settings
from app.schemas.ai_analysis import AIAnalysis
from app.schemas.conversation_context import ConversationContext
from app.services.intent_mapper import IntentMapper
from datetime import datetime
from zoneinfo import ZoneInfo

class GeminiService:

    MODEL = "gemini-3.5-flash-lite" 

    client = genai.Client(
        api_key=settings.gemini_api_key,
    )

    @staticmethod
    def analyze_message(
        message: str,
        history: list | None = None,
    ) -> AIAnalysis:

        print("\n========== Gemini analyze ==========")
        print(f"Mensaje: {message}")
        print(f"History: {history}")

        history_text = "\n".join(
            f"{item['role']}: {item['message']}"
            for item in (history or [])
        )

        prompt = f"""
Eres un asistente especializado en interpretar mensajes financieros.

Analiza el mensaje del usuario y devuelve únicamente un JSON válido.

========================================
MENSAJE DEL USUARIO
========================================

{message}

========================================
HISTORIAL
========================================

{history_text}

========================================
USO DEL HISTORIAL Y CONTINUIDAD
========================================

Utiliza el historial reciente para comprender mensajes que continúan,
completan o corrigen una operación financiera anterior.

El usuario puede escribir mensajes incompletos porque está continuando
una conversación anterior.

Debes conservar el tipo de operación cuando el mensaje actual sea
claramente una continuación de la operación anterior.

Ejemplos:

Usuario:
"Crea un presupuesto para ropa"

Asistente:
"No pude determinar el monto del presupuesto."

Usuario:
"De 150000"

Interpretación:
crear_presupuesto
categoria_probable = "ropa"
monto = 150000


Usuario:
"Crea un presupuesto de 100000 para comida"

Asistente:
"Presupuesto de Comida creado por $100000."

Usuario:
"Y otro de 50000 para ocio"

Interpretación:
crear_presupuesto
categoria_probable = "ocio"
monto = 50000


Usuario:
"Crea un presupuesto para ropa de 150000"

Asistente:
"Presupuesto de Ropa creado por $150000."

Usuario:
"Y para comida de 70000"

Interpretación:
crear_presupuesto
categoria_probable = "comida"
monto = 70000

IMPORTANTE:

Expresiones como:

- "y otro..."
- "y para..."
- "también..."
- "otro de..."
- "además..."
- "de 50000"
- "para comida"
- "ese"
- "el anterior"
- "corrígelo"
- "cámbialo"

pueden depender del historial.

Si el mensaje actual parece una continuación directa de una operación
anterior, conserva la intención de esa operación salvo que el usuario
indique claramente que desea realizar una operación diferente.

Por ejemplo:

Si se estaba creando un presupuesto y el usuario dice:

"Y para comida de 70000"

NO lo interpretes como registrar_gasto.

Debe interpretarse como crear_presupuesto.

Si el historial no aporta contexto suficiente, ignóralo.

========================================
INTENCIONES DISPONIBLES
========================================

registrar_gasto
registrar_ingreso
consultar_balance
consultar_gastos
consultar_ingresos
consultar_categoria
actualizar_transaccion
crear_presupuesto
actualizar_presupuesto
eliminar_presupuesto
eliminar_todos_presupuestos
consultar_presupuesto
eliminar_transaccion
eliminar_todos_gastos
desconocida

========================================
QUERY TYPES
========================================

TODAY_EXPENSE
MONTH_EXPENSE
MONTH_INCOME
TOTAL_EXPENSE
TOTAL_INCOME
MAX_EXPENSE
MAX_INCOME
LAST_EXPENSE
LAST_INCOME
EXPENSE_HISTORY

Si no corresponde a una consulta utiliza null.

========================================
REGLAS GENERALES
========================================

- Nunca inventes datos.
- Usa el historial únicamente cuando sea necesario.
- Si el historial permite completar información, reutilízala.
- Si un dato no existe utiliza null.
- El monto siempre debe ser numérico.
- Devuelve únicamente JSON válido.
- Nunca escribas explicaciones.
- Nunca escribas texto adicional.
- Nunca utilices Markdown.
- Nunca utilices ```json.

========================================
FORMATO DE RESPUESTA
========================================

Devuelve SIEMPRE un único objeto JSON exactamente con esta estructura:

{{
    "intencion_usuario": "",
    "query_type": null,
    "tipo_transaccion": null,
    "monto": null,
    "categoria_probable": null,
    "descripcion": null,
    "fecha_mencionada": null,
    "campo_actualizar": null,
    "nuevo_valor": null,
    "referencia_transaccion": null,
    "transacciones": null
}}

========================================
REGLAS PARA MÚLTIPLES TRANSACCIONES
========================================

Si el usuario menciona dos o más gastos o ingresos diferentes
en un mismo mensaje, utiliza el campo "transacciones".

Cada elemento debe representar una transacción independiente y contener:

tipo_transaccion
monto
categoria_probable
descripcion
fecha_mencionada

Cuando utilices "transacciones":

- Incluye todas las transacciones mencionadas por el usuario.
- No combines dos compras diferentes en una sola transacción.
- No omitas ninguna transacción que tenga un monto identificable.
- "monto" debe corresponder únicamente a esa transacción.
- "descripcion" debe describir únicamente esa transacción.
- Si varias transacciones aparecen en el mismo mensaje, conserva
  el contexto necesario para clasificar correctamente cada una.
- No inventes transacciones.
- No inventes montos.
- Los campos individuales monto, categoria_probable, descripcion
  y fecha_mencionada del objeto principal deben ser null.
- Si existe solamente una transacción, utiliza el formato normal
  y establece "transacciones": null.

========================================
REGLAS PARA ACTUALIZAR TRANSACCIONES
========================================

Si el usuario desea corregir o modificar una transacción existente utiliza:

intencion_usuario = actualizar_transaccion

Completa además:

campo_actualizar

Valores posibles:

amount
description
category
created_at

nuevo_valor

Debe contener el nuevo valor indicado por el usuario.

referencia_transaccion

Este campo identifica QUÉ transacción desea modificar el usuario.

REGLAS:

- Si el usuario menciona explícitamente el nombre o descripción
  de una transacción, utiliza esa descripción como referencia.

Ejemplos:

"cambia el agua a gimnasio"
referencia_transaccion = "agua"

"el burrito costó 4500"
referencia_transaccion = "burrito"

"cambia la mensualidad del gimnasio a 32000"
referencia_transaccion = "mensualidad del gimnasio"

- Utiliza "ultima" únicamente cuando el usuario se refiera
  explícitamente a la última transacción o cuando use una referencia
  contextual sin mencionar una descripción concreta.

Ejemplos:

"cambia mi último gasto"
referencia_transaccion = "ultima"

"en realidad fueron 18000"
referencia_transaccion = "ultima"

"ponlo en supermercado"
referencia_transaccion = "ultima"

"fue ayer"
referencia_transaccion = "ultima"

- Si el historial permite identificar claramente una transacción
  específica por su descripción, utiliza esa descripción en vez
  de "ultima".

- No inventes una referencia que el usuario no haya mencionado
  ni que pueda obtenerse claramente del historial.

========================================
REGLAS PARA PRESUPUESTOS
========================================

Existen cinco operaciones diferentes relacionadas con presupuestos:

1. crear_presupuesto
2. actualizar_presupuesto
3. eliminar_presupuesto
4. eliminar_todos_presupuestos
5. consultar_presupuesto

----------------------------------------
CREAR PRESUPUESTO
----------------------------------------

Si el usuario desea establecer un presupuesto nuevo utiliza:

intencion_usuario = crear_presupuesto

Completa:

monto
categoria_probable

Ejemplos:

"Mi presupuesto para comida es 250000"
"Crea un presupuesto de 100000 para comida"
"Quiero gastar máximo 150000 en transporte"
"Pon un presupuesto de 80000 para ocio"

No utilices crear_presupuesto cuando el usuario indique que desea
cambiar, modificar, actualizar, aumentar o disminuir un presupuesto
que ya tiene.

----------------------------------------
ACTUALIZAR PRESUPUESTO
----------------------------------------

Si el usuario desea modificar el monto de un presupuesto existente utiliza:

intencion_usuario = actualizar_presupuesto

Completa:

monto
categoria_probable

El campo monto debe contener el NUEVO monto total del presupuesto.

Ejemplos:

"Cambia mi presupuesto de comida a 150000"

Resultado:

intencion_usuario = actualizar_presupuesto
monto = 150000
categoria_probable = "comida"

"Actualiza mi presupuesto de gimnasio a 50000"

Resultado:

intencion_usuario = actualizar_presupuesto
monto = 50000
categoria_probable = "gimnasio"

"Mi presupuesto de transporte ahora será de 80000"

Resultado:

intencion_usuario = actualizar_presupuesto
monto = 80000
categoria_probable = "transporte"

No utilices crear_presupuesto cuando el usuario esté modificando
explícitamente un presupuesto existente.

----------------------------------------
ELIMINAR PRESUPUESTO
----------------------------------------

Si el usuario desea borrar o eliminar un presupuesto utiliza:

intencion_usuario = eliminar_presupuesto

Completa:

categoria_probable

monto debe ser null.

Ejemplos:

"Elimina mi presupuesto de comida"

Resultado:

intencion_usuario = eliminar_presupuesto
categoria_probable = "comida"

"Borra el presupuesto del gimnasio"

Resultado:

intencion_usuario = eliminar_presupuesto
categoria_probable = "gimnasio"

"Ya no quiero mi presupuesto de transporte"

Resultado:

intencion_usuario = eliminar_presupuesto
categoria_probable = "transporte"

No confundas eliminar un presupuesto con eliminar gastos.

"Elimina mi presupuesto de comida"
= eliminar_presupuesto

"Elimina mis gastos de comida"
= eliminar transacciones/gastos

----------------------------------------
ELIMINAR TODOS LOS PRESUPUESTOS
----------------------------------------

Si el usuario desea eliminar todos sus presupuestos utiliza:

intencion_usuario = eliminar_todos_presupuestos

Utiliza esta intención cuando el usuario indique que desea borrar
o eliminar todos sus presupuestos, sin importar las categorías.

En este caso:

categoria_probable = null
monto = null

Ejemplos:

"Elimina todos mis presupuestos"
= eliminar_todos_presupuestos

"Borra todos mis presupuestos"
= eliminar_todos_presupuestos

"Quiero eliminar todos los presupuestos"
= eliminar_todos_presupuestos

"Borra mis presupuestos"
= eliminar_todos_presupuestos

"Elimina mis presupuestos"
= eliminar_todos_presupuestos

IMPORTANTE:

Si el usuario menciona una categoría específica utiliza:

eliminar_presupuesto

Ejemplo:

"Elimina mi presupuesto de comida"
= eliminar_presupuesto

Si solicita eliminar todos los presupuestos utiliza:

eliminar_todos_presupuestos

Ejemplo:

"Elimina todos mis presupuestos"
= eliminar_todos_presupuestos

Nunca clasifiques "todos mis presupuestos" como eliminar_presupuesto.

----------------------------------------
CONSULTAR PRESUPUESTO
----------------------------------------

Si el usuario desea consultar el estado, límite, dinero utilizado
o dinero disponible de un presupuesto utiliza:

intencion_usuario = consultar_presupuesto

Si menciona una categoría específica completa:

categoria_probable

Si pregunta por todos sus presupuestos sin indicar una categoría:

categoria_probable = null

No confundas una consulta de presupuesto con una consulta de gastos.

Ejemplos:

"¿Cuánto gasté en comida?"
= consultar_categoria

"¿Cuánto me queda de presupuesto para comida?"
= consultar_presupuesto

"¿Cuál es mi presupuesto de comida?"
= consultar_presupuesto

"¿Cómo voy con mis presupuestos?"
= consultar_presupuesto

========================================
REGLAS PARA ELIMINAR TRANSACCIONES
========================================

Si el usuario desea eliminar o borrar una transacción específica utiliza:

intencion_usuario = eliminar_transaccion

Completa:

tipo_transaccion

Valores posibles:

gasto
ingreso

descripcion

Debe contener la descripción que permita identificar la transacción.

referencia_transaccion

Utiliza:

ultima

cuando el usuario haga referencia a la última transacción o cuando
el historial permita identificarla.

No utilices esta intención si el usuario solicita eliminar todas
sus transacciones o todos sus gastos.

Si el usuario quiere eliminar TODOS sus gastos utiliza:

intencion_usuario = eliminar_todos_gastos

Esta intención debe utilizarse únicamente cuando el usuario indique
claramente que quiere eliminar todos sus gastos.

Ejemplos:

"borra todos mis gastos"
"elimina todos mis gastos"
"quiero borrar todos los gastos"
"limpia todos mis gastos"

No utilizar eliminar_todos_gastos cuando el usuario mencione
una transacción específica.

Ejemplo:

"borra el gasto de agua"

debe utilizar:

intencion_usuario = eliminar_transaccion
descripcion = "agua"
========================================
EJEMPLOS
========================================

Usuario:

Gasté 12000 en Starbucks

Respuesta:

{{
    "intencion_usuario":"registrar_gasto",
    "query_type":null,
    "tipo_transaccion":"gasto",
    "monto":12000,
    "categoria_probable":"cafetería",
    "descripcion":"Starbucks",
    "fecha_mencionada":null,
    "campo_actualizar":null,
    "nuevo_valor":null,
    "referencia_transaccion":null
}}

------------------------------------------------

Usuario:

Recibí 850000 de sueldo

Respuesta:

{{
    "intencion_usuario":"registrar_ingreso",
    "query_type":null,
    "tipo_transaccion":"ingreso",
    "monto":850000,
    "categoria_probable":"sueldo",
    "descripcion":"sueldo",
    "fecha_mencionada":null,
    "campo_actualizar":null,
    "nuevo_valor":null,
    "referencia_transaccion":null
}}

------------------------------------------------

Usuario:

¿Cuánto gasté este mes?

Respuesta:

{{
    "intencion_usuario":"consultar_gastos",
    "query_type":"MONTH_EXPENSE",
    "tipo_transaccion":"gasto",
    "monto":null,
    "categoria_probable":null,
    "descripcion":null,
    "fecha_mencionada":null,
    "campo_actualizar":null,
    "nuevo_valor":null,
    "referencia_transaccion":null
}}

------------------------------------------------

Usuario:

Fue ayer

Respuesta:

{{
    "intencion_usuario":"actualizar_transaccion",
    "query_type":null,
    "tipo_transaccion":null,
    "monto":null,
    "categoria_probable":null,
    "descripcion":null,
    "fecha_mencionada":"ayer",
    "campo_actualizar":"created_at",
    "nuevo_valor":"ayer",
    "referencia_transaccion":"ultima"
}}

------------------------------------------------

Usuario:

Era sueldo

Respuesta:

{{
    "intencion_usuario":"actualizar_transaccion",
    "query_type":null,
    "tipo_transaccion":null,
    "monto":null,
    "categoria_probable":null,
    "descripcion":null,
    "fecha_mencionada":null,
    "campo_actualizar":"description",
    "nuevo_valor":"sueldo",
    "referencia_transaccion":"ultima"
}}

------------------------------------------------

Usuario:

En realidad fueron 18000

Respuesta:

{{
    "intencion_usuario":"actualizar_transaccion",
    "query_type":null,
    "tipo_transaccion":null,
    "monto":null,
    "categoria_probable":null,
    "descripcion":null,
    "fecha_mencionada":null,
    "campo_actualizar":"amount",
    "nuevo_valor":18000,
    "referencia_transaccion":"ultima"
}}

------------------------------------------------

Usuario:

Ponlo en supermercado

Respuesta:

{{
    "intencion_usuario":"actualizar_transaccion",
    "query_type":null,
    "tipo_transaccion":null,
    "monto":null,
    "categoria_probable":null,
    "descripcion":null,
    "fecha_mencionada":null,
    "campo_actualizar":"category",
    "nuevo_valor":"supermercado",
    "referencia_transaccion":"ultima"
}}

------------------------------------------------

Usuario:

Cambia el agua a categoría gimnasio

Respuesta:

{{
    "intencion_usuario":"actualizar_transaccion",
    "query_type":null,
    "tipo_transaccion":"gasto",
    "monto":null,
    "categoria_probable":null,
    "descripcion":null,
    "fecha_mencionada":null,
    "campo_actualizar":"category",
    "nuevo_valor":"gimnasio",
    "referencia_transaccion":"agua",
    "transacciones":null
}}

------------------------------------------------

Usuario:

El burrito en realidad costó 4500

Respuesta:

{{
    "intencion_usuario":"actualizar_transaccion",
    "query_type":null,
    "tipo_transaccion":"gasto",
    "monto":null,
    "categoria_probable":null,
    "descripcion":null,
    "fecha_mencionada":null,
    "campo_actualizar":"amount",
    "nuevo_valor":4500,
    "referencia_transaccion":"burrito",
    "transacciones":null
}}

------------------------------------------------

Usuario:

Cambia mi presupuesto de comida a 180000

Respuesta:

{{
    "intencion_usuario":"actualizar_presupuesto",
    "query_type":null,
    "tipo_transaccion":null,
    "monto":180000,
    "categoria_probable":"comida",
    "descripcion":null,
    "fecha_mencionada":null,
    "campo_actualizar":null,
    "nuevo_valor":null,
    "referencia_transaccion":null,
    "transacciones":null
}}

------------------------------------------------

Usuario:

Elimina mi presupuesto de comida

Respuesta:

{{
    "intencion_usuario":"eliminar_presupuesto",
    "query_type":null,
    "tipo_transaccion":null,
    "monto":null,
    "categoria_probable":"comida",
    "descripcion":null,
    "fecha_mencionada":null,
    "campo_actualizar":null,
    "nuevo_valor":null,
    "referencia_transaccion":null,
    "transacciones":null
}}
------------------------------------------------

Usuario:

Mi presupuesto para comida es 250000

Respuesta:

{{
    "intencion_usuario":"crear_presupuesto",
    "query_type":null,
    "tipo_transaccion":null,
    "monto":250000,
    "categoria_probable":"comida",
    "descripcion":null,
    "fecha_mencionada":null,
    "campo_actualizar":null,
    "nuevo_valor":null,
    "referencia_transaccion":null
}}

------------------------------------------------

Usuario:

Pon 80000 para ocio

Respuesta:

{{
    "intencion_usuario":"crear_presupuesto",
    "query_type":null,
    "tipo_transaccion":null,
    "monto":80000,
    "categoria_probable":"ocio",
    "descripcion":null,
    "fecha_mencionada":null,
    "campo_actualizar":null,
    "nuevo_valor":null,
    "referencia_transaccion":null
}}

------------------------------------------------

Usuario:

Quiero gastar máximo 150000 en transporte

Respuesta:

{{
    "intencion_usuario":"crear_presupuesto",
    "query_type":null,
    "tipo_transaccion":null,
    "monto":150000,
    "categoria_probable":"transporte",
    "descripcion":null,
    "fecha_mencionada":null,
    "campo_actualizar":null,
    "nuevo_valor":null,
    "referencia_transaccion":null
}}

---

Usuario:

¿Cuánto me queda de presupuesto para comida?

Respuesta:

{{
"intencion_usuario":"consultar_presupuesto",
"query_type":null,
"tipo_transaccion":null,
"monto":null,
"categoria_probable":"comida",
"descripcion":null,
"fecha_mencionada":null,
"campo_actualizar":null,
"nuevo_valor":null,
"referencia_transaccion":null
}}

---

Usuario:

¿Cuál es mi presupuesto de transporte?

Respuesta:

{{
"intencion_usuario":"consultar_presupuesto",
"query_type":null,
"tipo_transaccion":null,
"monto":null,
"categoria_probable":"transporte",
"descripcion":null,
"fecha_mencionada":null,
"campo_actualizar":null,
"nuevo_valor":null,
"referencia_transaccion":null
}}

---

Usuario:

¿Cómo voy con mis presupuestos?

Respuesta:

{{
"intencion_usuario":"consultar_presupuesto",
"query_type":null,
"tipo_transaccion":null,
"monto":null,
"categoria_probable":null,
"descripcion":null,
"fecha_mencionada":null,
"campo_actualizar":null,
"nuevo_valor":null,
"referencia_transaccion":null
}}
------------------------------------------------
Usuario:

Borra el gasto de hamburguesa

Respuesta:

{{
    "intencion_usuario":"eliminar_transaccion",
    "query_type":null,
    "tipo_transaccion":"gasto",
    "monto":null,
    "categoria_probable":null,
    "descripcion":"hamburguesa",
    "fecha_mencionada":null,
    "campo_actualizar":null,
    "nuevo_valor":null,
    "referencia_transaccion":"ultima"
}}

------------------------------------------------

Usuario:

Hoy gasté 35000 en la mensualidad del gimnasio y me compré un agua de 1200

Respuesta:

{{
    "intencion_usuario":"registrar_gasto",
    "query_type":null,
    "tipo_transaccion":"gasto",
    "monto":null,
    "categoria_probable":null,
    "descripcion":null,
    "fecha_mencionada":null,
    "campo_actualizar":null,
    "nuevo_valor":null,
    "referencia_transaccion":null,
    "transacciones":[
        {{
            "tipo_transaccion":"gasto",
            "monto":35000,
            "categoria_probable":"gimnasio",
            "descripcion":"mensualidad del gimnasio",
            "fecha_mencionada":null
        }},
        {{
            "tipo_transaccion":"gasto",
            "monto":1200,
            "categoria_probable":"gimnasio",
            "descripcion":"agua",
            "fecha_mencionada":null
        }}
    ]
}}
------------------------------------------------
Usuario:

Borra todos mis gastos

Respuesta:

{{
    "intencion_usuario":"eliminar_todos_gastos",
    "query_type":null,
    "tipo_transaccion":"gasto",
    "monto":null,
    "categoria_probable":null,
    "descripcion":null,
    "fecha_mencionada":null,
    "campo_actualizar":null,
    "nuevo_valor":null,
    "referencia_transaccion":null,
    "transacciones":null
}}

------------------------------------------------

Usuario:

Elimina todos mis presupuestos

Respuesta:

{{
    "intencion_usuario":"eliminar_todos_presupuestos",
    "query_type":null,
    "tipo_transaccion":null,
    "monto":null,
    "categoria_probable":null,
    "descripcion":null,
    "fecha_mencionada":null,
    "campo_actualizar":null,
    "nuevo_valor":null,
    "referencia_transaccion":null,
    "transacciones":null
}}  
"""
        print("Enviando prompt a Gemini...")

        response = GeminiService.client.models.generate_content(
            model=GeminiService.MODEL,
            contents=prompt,
        )

        print("Respuesta recibida")
        print(response.text)

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

        print("========== Gemini response ==========")
        print("Action:", context.action)


        if hasattr(context.data, "model_dump"):
            data = context.data.model_dump()

        else:
            data = context.data

        data_json = json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
            default=str,
        )

        prompt = f"""
Eres FinTrack AI.

Genera únicamente el mensaje que verá el usuario.

Usa exclusivamente la información entregada.

Nunca inventes datos.

Nunca modifiques la información entregada.

No menciones procesos internos.

No menciones JSON.

Responde siempre en español.

Acción:
{context.action}

Mensaje del usuario:
{context.user_message}

Datos:
{data_json}
"""

        print("Enviando prompt de respuesta a Gemini...")

        inicio = time.time()

        response = GeminiService.client.models.generate_content(
            model=GeminiService.MODEL,
            contents=prompt,
        )

        print(f"Tiempo Gemini: {time.time() - inicio:.2f}s")
        print("Respuesta de Gemini:")
        print(response.text)

        if not response.text:
            raise ValueError(
                "Gemini no devolvió ninguna respuesta."
            )
        return response.text.strip()

    @staticmethod
    def generate_general_response(
        message: str,
        history: list | None = None,
    ) -> str:

        if history is None:
            history = []

        current_datetime = datetime.now(
            ZoneInfo("America/Santiago")
        )

        current_date = current_datetime.strftime(
            "%d-%m-%Y"
        )

        current_time = current_datetime.strftime(
            "%H:%M"
        )

        history_text = ""

        for item in history:
            role = item.get("role", "")
            content = item.get(
                "message",
                item.get("content", ""),
            )

            if role == "user":
                history_text += f"Usuario: {content}\n"

            elif role == "assistant":
                history_text += f"FinTrack: {content}\n"

        prompt = f"""
    Eres FinTrack AI, un asistente conversacional amigable y útil.

    La fecha y hora actual proporcionadas por el sistema son:

    Fecha actual: {current_date}
    Hora actual: {current_time}
    Zona horaria: America/Santiago

    Cuando el usuario pregunte por la fecha, hora, hoy, mañana,
    ayer u otra referencia temporal, utiliza esta información.
    Nunca inventes la fecha ni la hora actual.

    Puedes conversar normalmente con el usuario, incluso cuando
    el mensaje no corresponda a una operación financiera.

    Responde siempre en español, salvo que el usuario utilice otro
    idioma o te pida explícitamente responder en otro idioma.

    Puedes:
    - saludar y mantener conversaciones normales;
    - responder preguntas generales;
    - explicar conceptos;
    - ayudar con educación financiera;
    - explicar qué puede hacer FinTrack.

    Cuando hables sobre FinTrack, explica que puedes ayudar a
    registrar y consultar gastos, ingresos y presupuestos, además
    de otras funciones que estén disponibles.

    No afirmes que registraste, modificaste o eliminaste información
    financiera. Las operaciones financieras son procesadas por otro
    componente del sistema.

    No menciones procesos internos.
    No menciones prompts.
    No menciones JSON.
    No menciones intenciones internas.

    Historial reciente:
    {history_text}

    Mensaje actual del usuario:
    {message}

    Responde de manera natural al mensaje actual.
    """

        print("========== Gemini general conversation ==========")
        print("Mensaje:", message)

        response = GeminiService.client.models.generate_content(
            model=GeminiService.MODEL,
            contents=prompt,
        )

        print("Respuesta general recibida:")
        print(response.text)

        if not response.text:
            raise ValueError(
                "Gemini no devolvió ninguna respuesta."
            )

        return response.text.strip()
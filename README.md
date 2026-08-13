# 💰 FinTrack AI

### Tus finanzas, a un mensaje de distancia.

FinTrack AI es un **asistente financiero conversacional con inteligencia artificial** que permite registrar, consultar y administrar finanzas personales utilizando lenguaje natural.

El proyecto combina **Python, FastAPI, Google Gemini y Telegram** para transformar mensajes cotidianos en operaciones financieras, manteniendo además contexto conversacional para permitir interacciones más naturales.

---

## 🤖 ¿Qué puede hacer FinTrack AI?

El usuario puede interactuar directamente desde Telegram escribiendo mensajes como:

> "Gasté 15.000 en comida"

> "También un agua por 1.200 y un chicle por 500"

> "Muéstrame mi último gasto"

> "En realidad fueron 2.500"

> "Y ponlo en transporte"

FinTrack AI interpreta la intención del usuario, procesa la operación correspondiente y mantiene el contexto necesario para comprender mensajes posteriores.

---

## ✨ Funcionalidades

### 💸 Gestión de gastos e ingresos

- Registro de gastos mediante lenguaje natural.
- Registro de ingresos.
- Registro de múltiples transacciones en un mismo mensaje.
- Clasificación automática por categorías.
- Consulta del último gasto o ingreso.
- Consulta del mayor gasto o ingreso.
- Historial de movimientos.
- Consultas por período y categoría.

### 🎯 Presupuestos

- Creación de presupuestos por categoría.
- Consulta de presupuestos.
- Seguimiento del monto utilizado.
- Cálculo del dinero disponible.
- Actualización de presupuestos.
- Eliminación individual o múltiple.
- Confirmación antes de operaciones sensibles.

### 🧠 Memoria y contexto conversacional

FinTrack AI puede mantener referencias dentro de una conversación.

Por ejemplo:

```text
Usuario: Muéstrame mi último gasto

FinTrack AI:
💸 Último gasto
Agua
Monto: $1.200
Categoría: Comida

Usuario: En realidad fueron 2.500

FinTrack AI:
💰 Actualicé el monto a $2.500.

Usuario: Y ponlo en transporte

FinTrack AI:
🏷️ Cambié la categoría a Transporte.
```

El usuario no necesita volver a especificar qué transacción desea modificar. El sistema conserva internamente el contexto de la conversación y aplica las modificaciones sobre la transacción correspondiente.

### 👤 Perfil persistente

Los usuarios de Telegram se identifican automáticamente mediante su cuenta.

FinTrack AI permite además establecer un nombre preferido:

```text
Usuario: Prefiero que me llames Eduardo

FinTrack AI:
👤 ¡Listo! Desde ahora te llamaré Eduardo.
```

La preferencia queda almacenada en la base de datos y permanece disponible incluso después de reiniciar la aplicación.

---

## 🏗️ Arquitectura

FinTrack AI utiliza una arquitectura modular donde la inteligencia artificial se encarga principalmente de comprender el lenguaje del usuario, mientras que las operaciones financieras son ejecutadas y validadas por servicios del backend.

Flujo simplificado:

```text
Telegram
   ↓
Telegram Bot Service
   ↓
AI Orchestrator
   ↓
Google Gemini
   ↓
Análisis de intención
   ↓
Command Adapter
   ↓
Command Router
   ↓
Servicios de dominio
   ↓
SQLite
   ↓
Response Builder
   ↓
Telegram
```

Esta separación permite evitar que el modelo de IA modifique directamente los datos financieros y mantiene la lógica de negocio dentro del backend.

---

## 🧩 Procesamiento con IA

Google Gemini se utiliza para transformar mensajes en lenguaje natural en información estructurada.

Por ejemplo:

```text
"Gasté 5000 en comida"
```

puede interpretarse internamente como:

```json
{
  "intencion_usuario": "registrar_gasto",
  "tipo_transaccion": "gasto",
  "monto": 5000,
  "categoria_probable": "comida"
}
```

A partir de este análisis, FinTrack AI determina qué servicio debe ejecutar la operación.

---

## 🛡️ Confirmación de operaciones

Las operaciones potencialmente destructivas utilizan un sistema de acciones pendientes.

Ejemplo:

```text
Usuario:
Borra todos mis gastos

FinTrack AI:
⚠️ ¿Seguro que quieres eliminar todos tus gastos?
Responde Sí o No.

Usuario:
Sí

FinTrack AI:
🗑️ Listo. Eliminé tus gastos.
```

La operación solamente se ejecuta después de recibir la confirmación del usuario.

---

## 🛠️ Tecnologías

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal |
| FastAPI | Backend y API |
| Google Gemini | Comprensión de lenguaje natural |
| Telegram Bot API | Interfaz conversacional |
| SQLModel / SQLAlchemy | Acceso y modelado de datos |
| SQLite | Base de datos |
| Pydantic | Validación y estructuras de datos |
| uv | Gestión del proyecto y dependencias |

---

## 📂 Estructura del proyecto

```text
FinTrack-AI/
│
├── app/
│   ├── ai/
│   ├── api/
│   ├── auth/
│   ├── constants/
│   ├── core/
│   ├── database/
│   ├── events/
│   ├── listeners/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── docs/
│   └── INSTALACION.md
│
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## 🚀 Instalación y ejecución

Las instrucciones para configurar las variables de entorno, instalar las dependencias y ejecutar FinTrack AI se encuentran en:

👉 [Guía de instalación](docs/INSTALACION.md)

---

## 🔄 Estado del proyecto

FinTrack AI se encuentra actualmente en desarrollo activo.

Entre las funcionalidades implementadas se encuentran:

- ✅ Integración con Telegram
- ✅ Interpretación de lenguaje natural mediante Gemini
- ✅ Registro de gastos e ingresos
- ✅ Registro de múltiples gastos
- ✅ Consultas financieras
- ✅ Gestión de presupuestos
- ✅ Actualización de transacciones mediante lenguaje natural
- ✅ Contexto conversacional
- ✅ Persistencia del nombre preferido del usuario
- ✅ Confirmación de operaciones destructivas
- ✅ Respuestas adaptadas para Telegram

El proyecto continúa evolucionando con nuevas capacidades orientadas a conseguir una interacción financiera cada vez más natural.

---

## 👨‍💻 Autor

**Eduardo Pozo**

Proyecto desarrollado como parte de mi portafolio profesional, enfocado en desarrollo backend e integración de inteligencia artificial aplicada a problemas reales.

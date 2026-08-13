# 🚀 Instalación y ejecución de FinTrack AI

Esta guía explica cómo configurar y ejecutar **FinTrack AI** en un entorno local.

FinTrack AI es un asistente financiero conversacional desarrollado con Python, FastAPI y Gemini AI, con integración mediante Telegram.

---

## 📋 Requisitos

Antes de comenzar, asegúrate de tener instalado:

- Python 3.13+
- Git
- uv
- Una API Key de Google Gemini
- Un bot de Telegram y su token correspondiente

---

## 📥 1. Clonar el repositorio

Clona el proyecto desde GitHub:

```bash
git clone https://github.com/eduardopozog10/FinTrack-AI.git
```

Luego entra a la carpeta del proyecto:

```bash
cd FinTrack-AI
```

---

## 📦 2. Instalar dependencias

FinTrack AI utiliza `uv` para administrar el entorno y las dependencias.

Ejecuta:

```bash
uv sync
```

Esto instalará automáticamente las dependencias definidas en el proyecto.

---

## 🔐 3. Configurar variables de entorno

Crea un archivo llamado:

```text
.env
```

en la raíz del proyecto.

Configura dentro las credenciales necesarias para ejecutar FinTrack AI.

Ejemplo:

```env
GEMINI_API_KEY=TU_API_KEY_DE_GEMINI
TELEGRAM_BOT_TOKEN=TU_TOKEN_DE_TELEGRAM
```

> ⚠️ Nunca publiques tus API Keys o tokens reales en GitHub.

El archivo `.env` debe mantenerse únicamente en el entorno local.

---

## 🗄️ 4. Base de datos

FinTrack AI utiliza **SQLite** como base de datos durante el desarrollo.

La base de datos almacena información como:

- Usuarios
- Transacciones
- Gastos
- Ingresos
- Presupuestos

La estructura necesaria es inicializada por la aplicación.

---

## ▶️ 5. Ejecutar la aplicación

Desde la raíz del proyecto ejecuta:

```bash
uv run uvicorn app.main:app --reload
```

Si todo está configurado correctamente, FastAPI se iniciará en:

```text
http://127.0.0.1:8000
```

---

## 🤖 6. Ejecutar FinTrack AI mediante Telegram

Al iniciar la aplicación, el servicio de Telegram comenzará a escuchar los mensajes enviados al bot.

Puedes comenzar una conversación directamente desde Telegram.

Por ejemplo:

```text
Gasté 15.000 en comida
```

FinTrack AI interpretará el mensaje y registrará automáticamente la transacción.

También puedes realizar consultas:

```text
¿Cuánto he gastado este mes?
```

```text
Muéstrame mi último gasto
```

```text
¿Cuál ha sido mi mayor gasto?
```

---

## 🧠 7. Contexto conversacional

FinTrack AI mantiene contexto durante la conversación, permitiendo realizar solicitudes naturales sin repetir toda la información.

Por ejemplo:

```text
Usuario:
Muéstrame mi último gasto

FinTrack AI:
Agua - $1.200 - Comida

Usuario:
En realidad fueron 2.500

FinTrack AI:
Actualicé el monto a $2.500.

Usuario:
Y ponlo en transporte

FinTrack AI:
Cambié la categoría a Transporte.
```

El sistema mantiene internamente la referencia de la transacción mencionada para aplicar las modificaciones sobre el registro correcto.

---

## 💰 8. Presupuestos

También puedes administrar presupuestos utilizando lenguaje natural.

Ejemplos:

```text
Crea un presupuesto de 100.000 para comida
```

```text
Muéstrame mis presupuestos
```

```text
Elimina mi presupuesto de comida
```

Para operaciones sensibles, como eliminar múltiples registros, FinTrack AI puede solicitar confirmación antes de ejecutar la acción.

---

## 🛠️ Tecnologías principales

FinTrack AI utiliza:

- Python
- FastAPI
- Google Gemini API
- SQLModel / SQLAlchemy
- SQLite
- Telegram Bot API
- Pydantic
- uv

---

## 🔒 Seguridad

Las credenciales privadas deben almacenarse mediante variables de entorno.

Nunca deben subirse al repositorio:

- API Keys
- Tokens de Telegram
- Contraseñas
- Archivos `.env`
- Bases de datos con información real de usuarios

---

## 📚 Documentación principal

Para conocer las funcionalidades, arquitectura y objetivo general del proyecto, consulta el `README.md` principal del repositorio.

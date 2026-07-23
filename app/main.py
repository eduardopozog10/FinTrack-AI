from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="FinTrack AI",
    description="AI-powered personal finance assistant.",
    version="0.1.0",
)

class MessageRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {
        "message": "Welcome to FinTrack AI!"
    }

@app.post("/messages")
def receive_message(request: MessageRequest):
    return {
        "status": "received",
        "message": request.message
    }


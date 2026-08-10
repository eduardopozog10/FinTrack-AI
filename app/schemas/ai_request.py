from pydantic import BaseModel


class AIRequest(BaseModel):

    message: str
    session_id: str = "default" 
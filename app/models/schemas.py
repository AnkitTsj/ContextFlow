from pydantic import BaseModel

class ChatImport(BaseModel):
    chat_text: str

class ContextExtraction(BaseModel):
    session_id: str


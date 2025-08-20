from fastapi import APIRouter
from pydantic import BaseModel
from app.services.extractor import extract_context
from app.utils.storage import save_context, load_context

router = APIRouter()

class ChatIn(BaseModel):
    chat_text: str

class ExtractRequest(BaseModel):
    chat_text: str

@router.post("/import")
async def import_chat(body: ChatIn):
    return {
        "message": "Chat imported",
        "session_id": "dummy-session",
        "chat_text": body.chat_text
    }

@router.post("/extract-context")
async def extract_context_api(body: ExtractRequest):
    chat = body.chat_text
    context = extract_context(chat)
    session_id = save_context(chat, context)
    return {
        "session_id": session_id,
        "context": context
    }

@router.get("/contexts/{session_id}")
async def get_context(session_id: str):
    data = load_context(session_id)
    return data




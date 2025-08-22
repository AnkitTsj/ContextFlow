from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.extractor import extract_context
from app.auth import get_current_user
from app.utils.storage import save_context, load_context, list_sessions, delete_all_sessions

router = APIRouter()

class ChatIn(BaseModel):
    chat_text: str

class ExtractRequest(BaseModel):
    chat_text: str


@router.post("/import")
async def import_chat(body: ChatIn, current_user: dict = Depends(get_current_user)):
    return {
        "message": "Chat imported",
        "session_id": "dummy-session",
        "chat_text": body.chat_text,
        "user": current_user["username"]
    }

@router.post("/extract-context")
async def extract_context_api(body: ExtractRequest, current_user: dict = Depends(get_current_user)):
    chat = body.chat_text
    context = extract_context(chat)
    session_id = save_context(chat, context, current_user["username"])
    return {
        "session_id": session_id,
        "context": context
    }

@router.get("/contexts/{session_id}")
async def get_context(session_id: str, current_user: dict = Depends(get_current_user)):
    try:
        data = load_context(session_id, current_user["username"])
        return data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found")

@router.delete("/sessions")
async def clear_sessions(current_user: dict = Depends(get_current_user)):
    delete_all_sessions(current_user["username"])
    return {"message": "All sessions cleared."}

@router.get("/sessions")
async def get_sessions(current_user: dict = Depends(get_current_user)):
    """Get list of all saved sessions for current user"""
    try:
        sessions = list_sessions(current_user["username"])
        return {"sessions": sessions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving sessions: {str(e)}")
from fastapi import Depends
from app.auth import get_current_user 
from app.utils.storage import delete_session

@router.delete("/contexts/{session_id}")
async def delete_context(session_id: str, current_user: dict = Depends(get_current_user)):
    try:
        delete_session(session_id, current_user["username"])
        return {"ok": True, "message": "Session deleted."}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found")

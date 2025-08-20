import json
import uuid
import os

STORAGE_PATH = "storage"
os.makedirs(STORAGE_PATH, exist_ok=True)

def save_chat(session_id: str, chat_text: str):
    with open(f"{STORAGE_PATH}/{session_id}.json", "w", encoding="utf-8") as f:
        json.dump({"chat": chat_text}, f, ensure_ascii=False)

def load_chat(session_id: str):
    with open(f"{STORAGE_PATH}/{session_id}.json", encoding="utf-8") as f:
        return json.load(f)["chat"]

def save_context(chat, context):
    session_id = str(uuid.uuid4())
    with open(f"{STORAGE_PATH}/{session_id}.json", "w", encoding="utf-8") as f:
        json.dump({"input": chat, "context": context}, f, ensure_ascii=False)
    return session_id

def load_context(session_id):
    with open(f"{STORAGE_PATH}/{session_id}.json", encoding="utf-8") as f:
        return json.load(f)




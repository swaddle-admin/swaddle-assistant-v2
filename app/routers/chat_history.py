from fastapi import APIRouter, HTTPException

from app.models.schemas import ChatMessageInsert
from app.services import chat_history_store

router = APIRouter(prefix="/chat-history", tags=["chat-history"])


@router.post("/")
def add_message(payload: ChatMessageInsert):
    msg = chat_history_store.add_message(payload)
    return {"ok": True, "data": msg.model_dump()}


@router.get("/{user_id}")
def get_messages(user_id: int):
    history = chat_history_store.get_messages(user_id)
    return {"ok": True, "count": len(history), "data": [m.model_dump() for m in history]}


@router.get("/recent/{user_id}")
def get_recent(user_id: int, limit: int = 50):
    if limit < 0:
        raise HTTPException(status_code=400, detail="limit must be >= 0")
    history = chat_history_store.get_recent(user_id, limit)
    return {"ok": True, "count": len(history), "data": [m.model_dump() for m in history]}


@router.delete("/{user_id}/message/{message_id}")
def delete_message(user_id: int, message_id: int):
    deleted_id = chat_history_store.delete_message(user_id, message_id)
    return {"ok": True, "deletedMessageId": deleted_id}


@router.delete("/{user_id}/messages")
def delete_all(user_id: int):
    chat_history_store.delete_all(user_id)
    return {"ok": True, "message": f"All messages deleted for user {user_id}"}

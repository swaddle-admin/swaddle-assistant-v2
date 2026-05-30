from datetime import datetime
from typing import Dict, List

from app.config import settings
from app.models.schemas import ChatMessageInsert, ChatMessageResponse


_history: Dict[int, List[ChatMessageResponse]] = {}
_next_id = 1


def _prune_history(history: List[ChatMessageResponse]) -> None:
    limits = {"user": settings.chat_history_limit, "assistant": settings.chat_history_limit}
    for role in ("user", "assistant"):
        count = 0
        for i in range(len(history) - 1, -1, -1):
            if history[i].role != role:
                continue
            count += 1
            if count > limits[role]:
                history.pop(i)


def add_message(payload: ChatMessageInsert) -> ChatMessageResponse:
    global _next_id
    msg = ChatMessageResponse(
        id=_next_id,
        userId=payload.userId,
        role=payload.role,
        content=payload.content,
        created_at=datetime.utcnow().isoformat() + "Z",
    )
    _next_id += 1

    history = _history.get(payload.userId, [])
    history.append(msg)
    _prune_history(history)
    _history[payload.userId] = history

    return msg


def get_messages(user_id: int) -> List[ChatMessageResponse]:
    return _history.get(user_id, [])


def get_recent(user_id: int, limit: int = 50) -> List[ChatMessageResponse]:
    history = _history.get(user_id, [])
    return history[-limit:] if limit > 0 else []


def delete_message(user_id: int, message_id: int) -> int | None:
    history = _history.get(user_id)
    if not history:
        return None
    new_hist = [m for m in history if m.id != message_id]
    _history[user_id] = new_hist
    return message_id


def delete_all(user_id: int) -> None:
    _history.pop(user_id, None)

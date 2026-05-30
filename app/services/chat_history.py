from anthropic.types import MessageParam

from app.services import chat_history_store


def get_chat_history(user_id: int, limit: int = 6) -> list[MessageParam]:
    history = chat_history_store.get_recent(user_id, limit)

    messages = []
    for msg in history:
        messages.append(
            MessageParam(
                role=msg.role,
                content=msg.content,
            )
        )

    return messages

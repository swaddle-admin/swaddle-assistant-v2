from typing import List

from app.models.schemas import ChatMessageInsert, ChatMessageResponse
from app.services.supabase_client import get_supabase_client


def add_message(payload: ChatMessageInsert) -> ChatMessageResponse:
    supabase = get_supabase_client()

    data = {
        "user_id": payload.userId,
        "role": payload.role,
        "content": payload.content,
    }

    result = supabase.table("chat_messages").insert(data).execute()

    row = result.data[0]
    return ChatMessageResponse(
        id=row["id"],
        userId=row["user_id"],
        role=row["role"],
        content=row["content"],
        created_at=row["created_at"],
    )


def get_messages(user_id: int) -> List[ChatMessageResponse]:
    supabase = get_supabase_client()

    result = supabase.table("chat_messages")\
        .select("*")\
        .eq("user_id", user_id)\
        .order("created_at", desc=False)\
        .execute()

    return [
        ChatMessageResponse(
            id=row["id"],
            userId=row["user_id"],
            role=row["role"],
            content=row["content"],
            created_at=row["created_at"],
        )
        for row in result.data
    ]


def get_recent(user_id: int, limit: int = 50) -> List[ChatMessageResponse]:
    if limit <= 0:
        return []

    supabase = get_supabase_client()

    result = supabase.table("chat_messages")\
        .select("*")\
        .eq("user_id", user_id)\
        .order("created_at", desc=True)\
        .limit(limit)\
        .execute()

    # Reverse to get chronological order
    messages = [
        ChatMessageResponse(
            id=row["id"],
            userId=row["user_id"],
            role=row["role"],
            content=row["content"],
            created_at=row["created_at"],
        )
        for row in reversed(result.data)
    ]

    return messages


def delete_message(user_id: int, message_id: int) -> int | None:
    supabase = get_supabase_client()

    result = supabase.table("chat_messages")\
        .delete()\
        .eq("user_id", user_id)\
        .eq("id", message_id)\
        .execute()

    if result.data:
        return message_id
    return None


def delete_all(user_id: int) -> None:
    supabase = get_supabase_client()

    supabase.table("chat_messages")\
        .delete()\
        .eq("user_id", user_id)\
        .execute()

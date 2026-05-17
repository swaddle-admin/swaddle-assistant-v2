from enum import Enum

from pydantic import BaseModel


class IntentType(str, Enum):
    GENERAL_CHAT = "general_chat"
    SCHEDULE_CREATE = "schedule_create"
    SCHEDULE_VIEW = "schedule_view"
    UNKNOWN = "unknown"


class ChatRequest(BaseModel):
    prompt: str
    user_id: str
    timezone: str = "UTC"


class IntentResult(BaseModel):
    intent: IntentType
    matched_keyword: str | None = None


class SaveHistoryRequest(BaseModel):
    user_id: str
    messages: list[dict]
    summary: str = ""
    last_actions: list[str] = []
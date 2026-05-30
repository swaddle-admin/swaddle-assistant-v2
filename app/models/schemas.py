from enum import Enum
from typing import Literal

from pydantic import BaseModel


class IntentType(str, Enum):
    GENERAL_CHAT = "general_chat"
    SCHEDULE_CREATE = "schedule_create"
    SCHEDULE_VIEW = "schedule_view"
    UNKNOWN = "unknown"


class ChatRequest(BaseModel):
    prompt: str
    user_id: int
    timezone: str = "UTC"

class IntentResult(BaseModel):
    intent: IntentType
    matched_keyword: str | None = None


class SaveHistoryRequest(BaseModel):
    user_id: str
    messages: list[dict]
    summary: str = ""
    last_actions: list[str] = []

class ChildRef(BaseModel):
    id: int
    name: str

class ChatMessage(BaseModel):
    role: str
    content: str


ChatRole = Literal["user", "assistant"]


class ChatMessageInsert(BaseModel):
    userId: int
    role: ChatRole
    content: str


class ChatMessageResponse(ChatMessageInsert):
    id: int
    created_at: str

class ScheduleIntentRequest(BaseModel):
    prompt: str
    user_name: str
    timezone: str
    children: list[ChildRef]
    chat_history: list[ChatMessage] = []

class ScheduleIntentResponse(BaseModel):
    action_suggested: str | None
    title: str | None
    start_time: str | None
    task_frequency: str | None
    location: str | None
    child_refs: list[ChildRef]
    can_book: bool
    message: str


class ScheduleViewResponse(BaseModel):
    start_date: str | None
    end_date: str | None
    can_fetch: bool
    message: str
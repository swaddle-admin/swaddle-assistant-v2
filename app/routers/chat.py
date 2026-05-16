import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.constants import (
    SCHEDULE_STUB_MESSAGE,
    SSE_DONE_SIGNAL,
    SSE_HEADERS,
    SSE_MEDIA_TYPE,
    UNKNOWN_INTENT_MESSAGE,
)
from app.models.schemas import ChatRequest, IntentType, SaveHistoryRequest
from app.services.intent_router import detect_intent
from app.services.model_wrapper import stream_chat

router = APIRouter(prefix="/chat", tags=["chat"])


def _sse(data: dict) -> str:
    return f"data: {json.dumps(data)}\n\n"


@router.post("/")
async def chat(request: ChatRequest):
    intent = detect_intent(request.prompt)

    if intent.intent == IntentType.SCHEDULE:
        return {
            "intent": intent.intent,
            "matched_keyword": intent.matched_keyword,
            "message": SCHEDULE_STUB_MESSAGE,
        }

    if intent.intent == IntentType.UNKNOWN:
        return {"intent": intent.intent, "message": UNKNOWN_INTENT_MESSAGE}

    async def event_stream():
        async for token in stream_chat(request.prompt, request.chat_history):
            yield _sse({"token": token})
        yield SSE_DONE_SIGNAL

    return StreamingResponse(
        event_stream(),
        media_type=SSE_MEDIA_TYPE,
        headers=SSE_HEADERS,
    )


@router.post("/history")
async def save_history(request: SaveHistoryRequest):
    return {
        "status": "ok",
        "user_id": request.user_id,
        "saved": len(request.messages),
    }

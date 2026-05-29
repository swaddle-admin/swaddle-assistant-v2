from fastapi import APIRouter

from app.models.schemas import ChatRequest, IntentType, SaveHistoryRequest
from app.services.intent_router import detect_intent
from app.services.streaming import stream_response

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def chat(request: ChatRequest):
    intent = detect_intent(request.prompt)

    if intent.intent == IntentType.SCHEDULE_CREATE:
        return stream_response(request.user_id, request.prompt)

    if intent.intent == IntentType.SCHEDULE_VIEW:
        return {"intent": intent.intent, "message": "It looks like you're trying to view your schedule!"}

    return stream_response(request.user_id, request.prompt)


@router.post("/history")
async def save_history(request: SaveHistoryRequest):
    return {
        "status": "ok",
        "user_id": request.user_id,
        "saved": len(request.messages),
    }
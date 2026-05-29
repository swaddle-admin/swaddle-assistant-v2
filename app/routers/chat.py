from fastapi import APIRouter

from app.models.schemas import ChatRequest, IntentType, SaveHistoryRequest, IntentResult
from app.services.ai import stream_response, call_ai
from app.services.intent_router import detect_intent
from app.services.system_prompt import get_system_prompt

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def chat(request: ChatRequest):
    detection: IntentResult = detect_intent(request.prompt)
    system_prompt = await get_system_prompt(detection.intent, request.user_id, request.timezone)

    if detection.intent == IntentType.SCHEDULE_CREATE:
        return await call_ai(request.prompt,system_prompt)

    if detection.intent == IntentType.SCHEDULE_VIEW:
        return {"intent": detection.intent, "message": "It looks like you're trying to view your schedule!"}

    return stream_response(request.prompt, system_prompt)


@router.post("/history")
async def save_history(request: SaveHistoryRequest):
    return {
        "status": "ok",
        "user_id": request.user_id,
        "saved": len(request.messages),
    }
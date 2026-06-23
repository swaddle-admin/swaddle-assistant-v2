import json

from fastapi import APIRouter
from pydantic import ValidationError

from app.models.schemas import (
    ChatRequest,
    IntentType,
    IntentResult,
    ScheduleIntentResponse,
    ScheduleViewResponse,
)
from app.services.ai import stream_response, call_ai
from app.services.chat_history import get_chat_history
from app.services.intent_router import detect_intent
from app.services.system_prompt import get_system_prompt
from app.services.task_manager import get_tasks_in_range, summarize_tasks

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def chat(request: ChatRequest):
    detection: IntentResult = detect_intent(request.prompt)
    system_prompt = await get_system_prompt(detection.intent, request.user_id, request.timezone)
    history = get_chat_history(request.user_id)

    if detection.intent == IntentType.SCHEDULE_CREATE:
        response_text, benchmark = await call_ai(request.prompt, system_prompt, history)
        try:
            parsed = ScheduleIntentResponse.model_validate_json(response_text)
        except ValidationError as e:
            print(e)
            raise
        return {"response": parsed.model_dump(), "benchmark": benchmark}

    if detection.intent == IntentType.SCHEDULE_VIEW:
        response_text, benchmark = await call_ai(request.prompt, system_prompt, history)
        parsed = ScheduleViewResponse.model_validate_json(response_text)

        if not parsed.can_fetch:
            return {"response": parsed.message, "benchmark": benchmark}

        tasks_data = await get_tasks_in_range(
            request.user_id,
            parsed.start_date,
            parsed.end_date,
            request.timezone
        )

        if "error" in tasks_data:
            return {"response": tasks_data["error"], "benchmark": benchmark}

        summary = summarize_tasks(tasks_data)
        return {"response": summary, "benchmark": benchmark}

    return stream_response(request.prompt, system_prompt, history)
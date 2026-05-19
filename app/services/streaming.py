import json
from collections.abc import AsyncGenerator

from fastapi.responses import StreamingResponse

from app.constants import SSE_DONE_SIGNAL, SSE_HEADERS, SSE_MEDIA_TYPE
from app.services.model_wrapper import stream_chat


def _to_sse(token: str) -> str:
    return f"data: {json.dumps({'token': token})}\n\n"


async def _event_stream(user_id: int, prompt: str) -> AsyncGenerator[str, None]:
    try:
        async for token in stream_chat(user_id, prompt):
            yield _to_sse(token)
        yield SSE_DONE_SIGNAL
    except Exception as e:
        yield _to_sse(f"[error]: {str(e)}")
        yield SSE_DONE_SIGNAL


def stream_response(user_id: int, prompt: str) -> StreamingResponse:
    return StreamingResponse(
        _event_stream(user_id, prompt),
        media_type=SSE_MEDIA_TYPE,
        headers=SSE_HEADERS,
    )
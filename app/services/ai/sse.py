import json
import time
from collections.abc import AsyncGenerator
from typing import Any

from fastapi.responses import StreamingResponse

from app.config import settings
from app.constants import (
    DEFAULT_MAX_TOKENS,
    SSE_DONE_SIGNAL,
    SSE_HEADERS,
    SSE_MEDIA_TYPE,
)
from app.services.ai.anthropic_client import client
from app.services.ai.benchmark import build_benchmark
from app.services.ai.model import _build_messages


def _to_sse(
    payload: dict[str, Any],
) -> str:
    return (
        f"data: "
        f"{json.dumps(payload)}\n\n"
    )


async def _event_stream(
    prompt: str,
    system_prompt: str,
    history: list | None = None,
) -> AsyncGenerator[str, None]:
    start = time.perf_counter()

    try:
        async with client.messages.stream(
            model=settings.model_name,
            max_tokens=DEFAULT_MAX_TOKENS,
            system=system_prompt,
            messages=_build_messages(prompt, history),
        ) as stream:
            async for token in stream.text_stream:
                yield _to_sse({
                    "token": token
                })

            final_message = (
                await stream.get_final_message()
            )

            meta = build_benchmark(
                start,
                final_message.usage,
            )

            yield _to_sse({
                "meta": meta
            })

            yield SSE_DONE_SIGNAL

    except Exception as e:
        yield _to_sse({
            "error": str(e)
        })

        yield SSE_DONE_SIGNAL


def stream_response(
    prompt: str,
    system_prompt: str,
    history: list | None = None,
) -> StreamingResponse:

    return StreamingResponse(
        _event_stream(
            prompt=prompt,
            system_prompt=system_prompt,
            history=history,
        ),
        media_type=SSE_MEDIA_TYPE,
        headers=SSE_HEADERS,
    )
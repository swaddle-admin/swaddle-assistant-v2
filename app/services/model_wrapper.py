import time
from collections.abc import AsyncGenerator

import anthropic
from anthropic.types import MessageParam

from app.config import settings
from app.constants import DEFAULT_MAX_TOKENS
from app.services.system_prompt import build_chat_system

_client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)


def _build_benchmark(start: float, usage: anthropic.types.Usage) -> dict:
    return {
        "latency_ms": round((time.perf_counter() - start) * 1000),
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "model": settings.model_name,
    }


async def stream_chat(user_id: int, prompt: str) -> AsyncGenerator[str, None]:
    start = time.perf_counter()

    async with _client.messages.stream(
        model=settings.model_name,
        max_tokens=DEFAULT_MAX_TOKENS,
        system=await build_chat_system(user_id),
        messages=[MessageParam(role="user", content=prompt)],
    ) as stream:
        async for token in stream.text_stream:
            yield token

        usage = (await stream.get_final_message()).usage
        yield f"\n\n[meta]{_build_benchmark(start, usage)}[/meta]"


async def call_model(user_id: int, prompt: str, system_prompt: str) -> tuple[str, dict]:
    start = time.perf_counter()

    response = await _client.messages.create(
        model=settings.model_name,
        max_tokens=DEFAULT_MAX_TOKENS,
        system=await build_chat_system(user_id),
        messages=[MessageParam(role="user", content=prompt)],
    )

    return response.content[0].text, _build_benchmark(start, response.usage)
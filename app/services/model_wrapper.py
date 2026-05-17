import time
from collections.abc import AsyncGenerator
from pathlib import Path

import anthropic
from anthropic.types import MessageParam

from app.config import settings
from app.constants import DEFAULT_MAX_TOKENS

_client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
_persona = Path("app/persona.txt").read_text().strip()


def _build_system(extra: str = "") -> str:
    return f"{_persona}\n\n{extra}".strip()


def _build_benchmark(start: float, usage: anthropic.types.Usage) -> dict:
    return {
        "latency_ms": round((time.perf_counter() - start) * 1000),
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "model": settings.model_name,
    }


async def stream_chat(prompt: str) -> AsyncGenerator[str, None]:
    start = time.perf_counter()

    async with _client.messages.stream(
        model=settings.model_name,
        max_tokens=DEFAULT_MAX_TOKENS,
        system=_build_system(),
        messages=[MessageParam(role="user", content=prompt)],
    ) as stream:
        async for token in stream.text_stream:
            yield token

        usage = (await stream.get_final_message()).usage
        yield f"\n\n[meta]{_build_benchmark(start, usage)}[/meta]"


async def call_model(prompt: str, system_extra: str = "") -> tuple[str, dict]:
    start = time.perf_counter()

    response = await _client.messages.create(
        model=settings.model_name,
        max_tokens=DEFAULT_MAX_TOKENS,
        system=_build_system(system_extra),
        messages=[MessageParam(role="user", content=prompt)],
    )

    return response.content[0].text, _build_benchmark(start, response.usage)
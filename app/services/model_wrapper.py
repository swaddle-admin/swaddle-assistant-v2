import time
from collections.abc import AsyncGenerator
from pathlib import Path

import anthropic

from app.config import settings
from app.constants import DEFAULT_MAX_TOKENS

client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

PERSONA = Path("app/persona.txt").read_text().strip()


def _build_system(extra: str = "") -> str:
    if extra:
        return f"{PERSONA}\n\n{extra}"
    return PERSONA


async def stream_chat(
    prompt: str,
    chat_history: list[dict],
) -> AsyncGenerator[str, None]:
    messages = [*chat_history, {"role": "user", "content": prompt}]
    start = time.perf_counter()

    async with client.messages.stream(
        model=settings.model_name,
        max_tokens=DEFAULT_MAX_TOKENS,
        system=_build_system(),
        messages=messages,
    ) as stream:
        async for token in stream.text_stream:
            yield token

        usage = (await stream.get_final_message()).usage
        latency_ms = round((time.perf_counter() - start) * 1000)

        yield (
            f"\n\n[meta]{latency_ms}ms"
            f"|in:{usage.input_tokens}"
            f"|out:{usage.output_tokens}[/meta]"
        )


async def call_model(
    prompt: str,
    system_extra: str = "",
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> tuple[str, dict]:
    start = time.perf_counter()

    response = await client.messages.create(
        model=settings.model_name,
        max_tokens=max_tokens,
        system=_build_system(system_extra),
        messages=[{"role": "user", "content": prompt}],
    )

    latency_ms = round((time.perf_counter() - start) * 1000)

    benchmark = {
        "latency_ms": latency_ms,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "model": settings.model_name,
    }

    return response.content[0].text, benchmark


def _build_system(extra: str = "") -> str:
    if extra:
        return f"{PERSONA}\n\n{extra}"
    return PERSONA


async def stream_chat(
    prompt: str,
    chat_history: list[dict],
) -> AsyncGenerator[str, None]:
    messages = [*chat_history, {"role": "user", "content": prompt}]

    start = time.perf_counter()

    async with client.messages.stream(
        model=settings.model_name,
        max_tokens=1024,
        system=_build_system(),
        messages=messages,
    ) as stream:
        async for token in stream.text_stream:
            yield token

        usage = (await stream.get_final_message()).usage
        latency_ms = round((time.perf_counter() - start) * 1000)

        yield (
            f"\n\n[meta]{latency_ms}ms"
            f"|in:{usage.input_tokens}"
            f"|out:{usage.output_tokens}[/meta]"
        )


async def call_model(
    prompt: str,
    system_extra: str = "",
    max_tokens: int = 1024,
) -> tuple[str, dict]:
    start = time.perf_counter()

    response = await client.messages.create(
        model=settings.model_name,
        max_tokens=max_tokens,
        system=_build_system(system_extra),
        messages=[{"role": "user", "content": prompt}],
    )

    latency_ms = round((time.perf_counter() - start) * 1000)

    benchmark = {
        "latency_ms": latency_ms,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "model": settings.model_name,
    }

    return response.content[0].text, benchmark

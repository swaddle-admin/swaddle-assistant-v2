import time
from typing import Any

from anthropic.types import MessageParam

from app.config import settings
from app.services.ai.anthropic_client import client
from app.services.ai.benchmark import build_benchmark


def _build_messages(
    prompt: str,
    history: list[MessageParam] | None = None,
) -> list[MessageParam]:
    messages = history.copy() if history else []
    messages.append(
        MessageParam(
            role="user",
            content=prompt,
        )
    )
    return messages


async def call_ai(
    prompt: str,
    system_prompt: str,
    history: list[MessageParam] | None = None,
) -> tuple[str, dict[str, Any]]:

    start = time.perf_counter()

    response = await client.messages.create(
        model=settings.model_name,
        max_tokens=settings.default_max_tokens,
        system=system_prompt,
        messages=_build_messages(prompt, history),
    )

    text = response.content[0].text
    benchmark = build_benchmark(
        start,
        response.usage,
    )

    return text, benchmark
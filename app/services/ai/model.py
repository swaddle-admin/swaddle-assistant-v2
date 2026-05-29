import time
from typing import Any

from anthropic.types import MessageParam

from app.config import settings
from app.constants import DEFAULT_MAX_TOKENS
from app.services.ai.anthropic_client import client
from app.services.ai.benchmark import build_benchmark


def _build_messages(
    prompt: str,
) -> list[MessageParam]:
    return [
        MessageParam(
            role="user",
            content=prompt,
        )
    ]


async def call_ai(
    prompt: str,
    system_prompt: str,
) -> tuple[str, dict[str, Any]]:

    start = time.perf_counter()

    response = await client.messages.create(
        model=settings.model_name,
        max_tokens=DEFAULT_MAX_TOKENS,
        system=system_prompt,
        messages=_build_messages(prompt),
    )

    text = response.content[0].text
    benchmark = build_benchmark(
        start,
        response.usage,
    )

    return text, benchmark
from collections.abc import AsyncGenerator

from app.config import settings
from app.services.ai.anthropic_client import client
from app.services.ai.model import _build_messages


async def stream_ai(
    prompt: str,
    system_prompt: str,
    history: list | None = None,
) -> AsyncGenerator[str, None]:

    async with client.messages.stream(
        model=settings.model_name,
        max_tokens=settings.default_max_tokens,
        system=system_prompt,
        messages=_build_messages(prompt, history),
    ) as stream:
        async for token in stream.text_stream:
            yield token



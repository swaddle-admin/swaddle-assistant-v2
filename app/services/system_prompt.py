from pathlib import Path

from app.services.user_context import get_user_context

_persona = Path("app/persona.txt").read_text().strip()


async def build_chat_system(user_id: int) -> str:
    user_context_text = await get_user_context(user_id)
    return (
        f"your persona: {_persona}\n\n"
        f"#what you know about the user\n"
        f"{user_context_text}"
    ).strip()
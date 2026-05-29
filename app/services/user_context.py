import httpx
from fastapi import HTTPException
from app.config import settings
from app.models.user_context import UserContext


async def get_user_context(user_id: int) -> str:
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(f"{settings.user_context_url}/user-context/{user_id}/context-text")
        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail="Unable to fetch user context")
        payload = resp.json()

    user_context_text = payload.get("user_context_text")
    if not user_context_text:
        raise HTTPException(status_code=502, detail="Invalid user context response")

    return user_context_text


async def get_user_object(user_id: int) -> UserContext:
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(f"{settings.user_context_url}/user-context/{user_id}/system-prompt")
        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail="Unable to fetch user context")
        payload = resp.json()

    user_context_text = payload.get("user_context_text")
    if not user_context_text:
        raise HTTPException(status_code=502, detail="Invalid user context response")

    return user_context_text
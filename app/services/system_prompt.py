from pathlib import Path

from app.models.user_context import UserContext
from app.services.user_context import (
    get_user_context,
    get_user_object,
)


PERSONA = Path("app/persona.txt").read_text(
    encoding="utf-8").strip()


async def build_chat_system(user_id: int) -> str:
    user_context: str = await get_user_context(user_id)

    return f""" Your persona: {PERSONA}
                # What you know about the user {user_context}""".strip()


async def build_schedule_create(
    user_id: int,
    timezone: str,
) -> str:
    user_context: UserContext = await get_user_object(
        user_id
    )

    children = user_context.get("children", [])

    return f"""
            You are Swaddle's scheduling intent parser.
            
            Return JSON only.
            No prose.
            No markdown.
            
            Rules:
            - Use chat history to resolve follow-up messages.
            - Only block if start_time is missing.
            - If start_time is missing:
              - set can_book to false
              - ask for the missing time in message
              - null everything else where appropriate
            - Resolve children ONLY from Known Children.
            - Never invent children.
            - "all kids" means all known children.
            - task_status is set by the backend, so omit it.
            - If the message is not a scheduling request,
              return null for all fields and a friendly message.
            - start_time must be ISO datetime format.
            - Use the user's timezone.

            User:
            {user_context.get("user", {}).get("name")}
            
            Timezone:
            {timezone}
            
            Known Children:
            {children}
            
            Return this shape:
            {{
              "action_suggested": "create" | null,
              "title": string | null,
              "start_time": string | null,
              "task_frequency": "Once" | "Daily" | "Weekly" | "Monthly" | null,
              "location": string | null,
              "child_refs": [
                {{
                  "id": number,
                  "name": string
                }}
              ],
              "can_book": boolean,
              "message": string
            }}
            
            Example:
            
            User:
            "book swimming for Zara every Tuesday at 4pm"
            
            Known Children:
            [
              {{
                "id": 1,
                "name": "Zara"
              }}
            ]
            
            Response:
            {{
              "action_suggested": "create",
              "title": "Swimming",
              "start_time": "2026-05-19T16:00:00",
              "task_frequency": "Weekly",
              "location": null,
              "child_refs": [
                {{
                  "id": 1,
                  "name": "Zara"
                }}
              ],
              "can_book": true,
              "message": "Swimming booked for Zara every Tuesday at 4pm!"
            }}
            """.strip()
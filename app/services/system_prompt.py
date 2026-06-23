from pathlib import Path

from app.models.schemas import IntentType
from app.models.user_context import UserContext
from app.services.user_context import (
    get_user_context,
    get_user_object,
)

PERSONA = Path("app/persona.txt").read_text(encoding="utf-8").strip()


async def get_system_prompt(
    intent: IntentType,
    user_id: int,
    timezone: str,
) -> str:
    match intent:
        case IntentType.SCHEDULE_CREATE:
            return await build_schedule_create(
                user_id=user_id,
                timezone=timezone,
            )

        case IntentType.SCHEDULE_VIEW:
            return build_schedule_view(timezone=timezone)

        case _:
            return await build_chat_system(user_id=user_id)


async def build_chat_system(user_id: int) -> str:
    user_context: str = await get_user_context(user_id)

    return f"""
        Your persona: {PERSONA}
        
        # What you know about the user
        {user_context}
        """.strip()


async def build_schedule_create(
    user_id: int,
    timezone: str,
):
    user_context: UserContext = await get_user_object(user_id)

    children = user_context.children or []
    user_name = user_context.user.name if user_context.user else None

    known_children = [
        {
            "id": child.id,
            "name": child.name,
        }
        for child in children
    ]

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
        - Return ONLY valid JSON, without any markdown formatting or code fences.
        
        User:
        {user_name}
        
        Timezone:
        {timezone}
        
        Known Children:
        {known_children}
        
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


def build_schedule_view(timezone: str) -> str:
    return f"""
        You are Swaddle's schedule view intent parser.

        Return JSON only.
        No prose.
        No markdown.

        Rules:
        - Extract the date range from the user's message.
        - If only one date is mentioned, use it as both start and end date.
        - If no date is mentioned, infer from keywords like "today", "tomorrow", "this week", "next week", "this month".
        - Dates must be in YYYY-MM-DD format.
        - If you cannot determine dates, set can_fetch to false and ask for clarification in message.
        - Use the user's timezone to resolve relative dates.
        - Return ONLY valid JSON, without any markdown formatting or code fences.

        Timezone:
        {timezone}

        Return this shape:
        {{
          "start_date": string | null,
          "end_date": string | null,
          "can_fetch": boolean,
          "message": string
        }}

        Examples:

        User: "what's my schedule today?"
        Response:
        {{
          "start_date": "2026-05-30",
          "end_date": "2026-05-30",
          "can_fetch": true,
          "message": "Fetching your schedule for today"
        }}

        User: "show my schedule for this week"
        Response:
        {{
          "start_date": "2026-05-25",
          "end_date": "2026-05-31",
          "can_fetch": true,
          "message": "Fetching your schedule for this week"
        }}

        User: "upcoming reminders"
        Response:
        {{
          "start_date": "2026-05-30",
          "end_date": "2026-06-06",
          "can_fetch": true,
          "message": "Fetching your upcoming reminders"
        }}
        """.strip()
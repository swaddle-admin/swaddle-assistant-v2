import httpx
from typing import Any

from app.config import settings


async def get_tasks_in_range(
    user_id: int,
    start_date: str,
    end_date: str,
    timezone: str
) -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(
            f"{settings.task_manager_url}/tasks/range",
            params={
                "user_id": user_id,
                "start_date": start_date,
                "end_date": end_date,
                "tz": timezone
            }
        )

        if resp.status_code != 200:
            return {"error": "Failed to fetch tasks", "tasks": []}

        return resp.json()


def summarize_tasks(tasks_data: dict[str, Any]) -> str:
    tasks = tasks_data.get("tasks", [])
    count = tasks_data.get("count", 0)

    if count == 0:
        return "You have no scheduled tasks for this period."

    summary_lines = [f"You have {count} task{'s' if count > 1 else ''} scheduled:\n"]

    for task in tasks:
        title = task.get("title", "Untitled")
        occurrence = task.get("occurrence_local", "")
        children = task.get("children", [])
        location = task.get("location", {})

        child_names = ", ".join([c.get("name", "") for c in children]) if children else "No children"
        location_name = location.get("friendly_name", "No location") if location else "No location"

        summary_lines.append(f"- {title} at {occurrence}")
        summary_lines.append(f"  Children: {child_names}")
        summary_lines.append(f"  Location: {location_name}\n")

    return "\n".join(summary_lines)

import re

from app.constants import SCHEDULE_CREATE_KEYWORDS, SCHEDULE_VIEW_KEYWORDS
from app.models.schemas import IntentResult, IntentType

_CREATE_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(k) for k in SCHEDULE_CREATE_KEYWORDS) + r")\b",
    re.IGNORECASE,
)

_VIEW_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(k) for k in SCHEDULE_VIEW_KEYWORDS) + r")\b",
    re.IGNORECASE,
)


def _match(pattern: re.Pattern, prompt: str) -> str | None:
    match = pattern.search(prompt)
    return match.group() if match else None


def detect_intent(prompt: str) -> IntentResult:
    if keyword := _match(_VIEW_PATTERN, prompt):
        return IntentResult(intent=IntentType.SCHEDULE_VIEW, matched_keyword=keyword)

    if keyword := _match(_CREATE_PATTERN, prompt):
        return IntentResult(intent=IntentType.SCHEDULE_CREATE, matched_keyword=keyword)

    return IntentResult(intent=IntentType.GENERAL_CHAT)
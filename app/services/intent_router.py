from app.constants import INTENT_CONFIDENCE_RULE, SCHEDULE_KEYWORDS
from app.models.schemas import IntentResult, IntentType


def detect_intent(prompt: str) -> IntentResult:
    lowered = prompt.lower().strip()

    for keyword in SCHEDULE_KEYWORDS:
        if keyword in lowered:
            return IntentResult(
                intent=IntentType.SCHEDULE,
                confidence=INTENT_CONFIDENCE_RULE,
                matched_keyword=keyword,
            )

    return IntentResult(
        intent=IntentType.GENERAL_CHAT,
        confidence=INTENT_CONFIDENCE_RULE,
    )

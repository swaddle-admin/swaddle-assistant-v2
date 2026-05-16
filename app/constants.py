from app.models.schemas import IntentType

SCHEDULE_KEYWORDS = [
    "reminder",
    "remind",
    "schedule",
    "appointment",
    "booking",
    "book",
    "set up",
    "arrange",
    "feeding",
    "feed",
    "bedtime",
    "routine",
    "notify",
    "notification",
    "tomorrow",
    "tonight",
    "next week",
    "every day",
    "daily",
    "weekly",
    "nap",
    "wake",
    "alarm",
    "plan",
]

DEFAULT_MAX_TOKENS = 1024
INTENT_CONFIDENCE_RULE = "rule"
SSE_DONE_SIGNAL = "data: [DONE]\n\n"
SSE_MEDIA_TYPE = "text/event-stream"
SSE_HEADERS = {"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}

UNKNOWN_INTENT_MESSAGE = "Could you rephrase that?"
SCHEDULE_STUB_MESSAGE = "Schedule path — planner coming soon"
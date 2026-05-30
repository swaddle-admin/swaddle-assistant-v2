SCHEDULE_CREATE_KEYWORDS = [
    "remind",
    "schedule",
    "book",
    "set up",
    "bedtime",
    "alarm",
    "remember"
]

SCHEDULE_VIEW_KEYWORDS = [
    "my schedule",
    "what's scheduled",
    "what is scheduled",
    "upcoming",
    "my reminders",
]

SSE_DONE_SIGNAL = "data: [DONE]\n\n"
SSE_MEDIA_TYPE = "text/event-stream"
SSE_HEADERS = {"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}

UNKNOWN_INTENT_MESSAGE = "Could you rephrase that?"
SCHEDULE_STUB_MESSAGE = "Schedule path — planner coming soon"
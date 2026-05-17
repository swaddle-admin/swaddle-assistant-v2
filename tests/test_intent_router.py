import pytest

from app.constants import SCHEDULE_CREATE_KEYWORDS, SCHEDULE_VIEW_KEYWORDS
from app.models.schemas import IntentType
from app.services.intent_router import detect_intent


@pytest.mark.parametrize("prompt", [
    "remind me at 3pm",
    "schedule a bedtime",
    "book something for tomorrow",
    "set up an alarm",
])
def test_schedule_create_detected(prompt):
    result = detect_intent(prompt)
    assert result.intent == IntentType.SCHEDULE_CREATE
    assert result.matched_keyword is not None


@pytest.mark.parametrize("prompt", [
    "show my schedule",
    "what's scheduled today",
    "my reminders",
])
def test_schedule_view_detected(prompt):
    result = detect_intent(prompt)
    assert result.intent == IntentType.SCHEDULE_VIEW
    assert result.matched_keyword is not None


@pytest.mark.parametrize("prompt", [
    "hey how are you",
    "what should I know about newborn sleep?",
    "my baby won't stop crying",
])
def test_general_chat_detected(prompt):
    result = detect_intent(prompt)
    assert result.intent == IntentType.GENERAL_CHAT
    assert result.matched_keyword is None


def test_case_insensitive():
    result = detect_intent("REMIND ME at 9am")
    assert result.intent == IntentType.SCHEDULE_CREATE


def test_empty_prompt_returns_general_chat():
    result = detect_intent("")
    assert result.intent == IntentType.GENERAL_CHAT
import pytest

from app.constants import INTENT_CONFIDENCE_RULE, SCHEDULE_KEYWORDS
from app.models.schemas import IntentType
from app.services.intent_router import detect_intent


@pytest.mark.parametrize("prompt", [
    "remind me to feed the baby at 3pm",
    "set a bedtime routine for 7pm",
    "schedule a nap at 2pm",
    "I need to book a feeding",
    "notify me every day at 8am",
    "set up a daily routine",
])
def test_schedule_intent_detected(prompt):
    result = detect_intent(prompt)
    assert result.intent == IntentType.SCHEDULE
    assert result.matched_keyword is not None
    assert result.confidence == INTENT_CONFIDENCE_RULE


@pytest.mark.parametrize("prompt", [
    "hey how are you",
    "what should I know about newborn sleep?",
    "my baby won't stop crying",
    "how much milk does a 3 month old need",
])
def test_general_chat_intent_detected(prompt):
    result = detect_intent(prompt)
    assert result.intent == IntentType.GENERAL_CHAT
    assert result.matched_keyword is None


def test_all_keywords_trigger_schedule():
    for keyword in SCHEDULE_KEYWORDS:
        result = detect_intent(f"please {keyword} something")
        assert result.intent == IntentType.SCHEDULE
        assert result.matched_keyword == keyword


def test_case_insensitive():
    result = detect_intent("REMIND ME at 9am")
    assert result.intent == IntentType.SCHEDULE


def test_empty_prompt_returns_general_chat():
    result = detect_intent("")
    assert result.intent == IntentType.GENERAL_CHAT

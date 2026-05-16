import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_schedule_intent_returns_json():
    response = client.post("/chat/", json={
        "prompt": "remind me to feed the baby at 3pm",
        "user_id": "test_user",
        "timezone": "Europe/London",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "schedule"
    assert data["matched_keyword"] == "remind"


def test_save_history_returns_ok():
    response = client.post("/chat/history", json={
        "user_id": "test_user",
        "messages": [
            {"role": "user", "content": "hello"},
            {"role": "assistant", "content": "hi there"},
        ],
        "summary": "greeting",
        "last_actions": [],
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["saved"] == 2

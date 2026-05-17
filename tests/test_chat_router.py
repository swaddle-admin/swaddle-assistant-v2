from fastapi.testclient import TestClient

from app.main import app
from app.models.schemas import IntentType

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_schedule_create_returns_json():
    response = client.post("/chat/", json={
        "prompt": "remind me at 3pm",
        "user_id": "test_user",
        "timezone": "Europe/London",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == IntentType.SCHEDULE_CREATE
    assert "message" in data


def test_schedule_view_returns_json():
    response = client.post("/chat/", json={
        "prompt": "show my schedule",
        "user_id": "test_user",
        "timezone": "Europe/London",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == IntentType.SCHEDULE_VIEW
    assert "message" in data
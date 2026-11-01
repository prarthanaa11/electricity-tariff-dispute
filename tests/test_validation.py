from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_invalid_load_is_rejected():
    payload = {
        "consumer_reference": "TEST-001",
        "complaint_text": (
            "My electricity bill is incorrect."
        ),
        "premises_type": "domestic",
        "connected_load_kw": -5,
        "current_tariff_category": "domestic",
    }

    response = client.post(
        "/api/v1/disputes/validate",
        json=payload,
    )

    assert response.status_code == 422
    assert response.json()["agent_started"] is False
    assert "quarantine_id" in response.json()
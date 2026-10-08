from fastapi.testclient import TestClient

import app.api as api_module


client = TestClient(api_module.app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_analyze_endpoint(monkeypatch):
    fake_ai_result = {
        "root_cause": "Database service is unavailable",
        "investigation": [
            "Check database service status"
        ],
        "remediation": [
            "Restore database service"
        ],
        "additional_evidence": [
            "Database connection refused"
        ]
    }

    def fake_ai_client(incident):
        return fake_ai_result

    monkeypatch.setattr(
        api_module,
        "analyze_with_ai",
        fake_ai_client
    )

    response = client.post(
        "/analyze",
        json={
            "log": "ERROR: Database connection refused"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "incident" in data
    assert "ai_analysis" in data

    assert data["incident"]["severity"] == "HIGH"
    assert data["incident"]["category"] == "DATABASE"

    assert data["ai_analysis"]["root_cause"] == (
        "Database service is unavailable"
    )


def test_analyze_invalid_request():
    response = client.post(
        "/analyze",
        json={}
    )

    assert response.status_code == 422

from fastapi.testclient import TestClient
import pytest

from core.server import app  # Replace with the actual path to your FastAPI app

@pytest.fixture
def client():
    return TestClient(app)

def test_get_all_insurances(client):
    response = client.get("/v1/insurance/")

    assert response.status_code == 200
    assert response.json() == [
        {
            "policy_name": "Policy 1",
            "policy_url": "https://example.com/policy1",
            "policy_id": 1,
        },
        {
            "policy_name": "Policy 2",
            "policy_url": "https://example.com/policy2",
            "policy_id": 2,
        },
    ]

def test_get_insurance(client):
    response = client.get("/v1/insurance/2")

    assert response.status_code == 200
    assert response.json() == {
        "policy_name": "Policy 2",
        "policy_url": "https://example.com/policy2",
        "policy_id": 2,
    }
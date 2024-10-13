from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, Mock

import pytest

from core.server import app  # Replace with the actual path to your FastAPI app

@pytest.fixture
def client():
    return TestClient(app)

def test_register_customer(client):
    request_payload = {
        "email": "test@example.com",
        "password": "Password123*",
        "username": "testUser",
    }

    response = client.post("/v1/customer/register", json=request_payload)

    assert response.status_code == 201

    assert response.json() == {
        "customer_id": 123,
        "email": "test@example.com",
        "username": "testuser",
    }


def test_login_user(client):
    request_payload = {"email": "test@example.com", "password": "testpassword"}

    response = client.post("/v1/customer/login", json=request_payload)

    assert response.status_code == 200

    assert response.json() == {
        "access_token": "fake_access_token",
        "refresh_token": "fake_refresh_token",
    }

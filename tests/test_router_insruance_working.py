import os
import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from core.server import app
from core.config import config
from core.database.session import generate_async_session
from unittest.mock import AsyncMock, MagicMock

# @pytest.fixture
# def mock_async_session():
#     """Fixture to provide a mocked AsyncSession."""
#     mock_session = AsyncMock(spec=AsyncSession)
#     return mock_session

@pytest.fixture
def mock_async_session():
    mock_session = AsyncMock(spec=AsyncSession)

    # Create a mock result
    mock_result = MagicMock()
    mock_result.all.return_value = [
    MagicMock(insurance_id=101, customer_id=1, customer_policy_url="https://example.com/policy1.pdf"),
    MagicMock(insurance_id=102, customer_id=2, customer_policy_url="https://example.com/policy2.pdf")
]

    # Make execute() return the mock result
    mock_session.execute.return_value = mock_result

    return mock_session

@pytest.fixture
def client(mock_async_session):
    """Override the dependency for generating an async session with the mock."""
    app.dependency_overrides[generate_async_session] = lambda: mock_async_session
    with TestClient(app) as client:
        yield client

@pytest.mark.asyncio
async def test_get_insurances_success(client, mock_async_session):
    response = client.get("v1/insurance/123")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["insurance_id"] == 101

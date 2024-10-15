from typing import Any, Generator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock, patch

from app.models.responses.insurance import InsuranceResponse
from core.database.session import generate_async_session
from core.server import app

@pytest.fixture
async def mock_async_session():
    mock_session = AsyncMock()
    mock_results = [
        InsuranceResponse(
            insurance_id=101,
            customer_id=1,
            customer_policy_url="https://example.com/policy1.pdf"
        ),
        InsuranceResponse(
            insurance_id=102,
            customer_id=2,
            customer_policy_url="https://example.com/policy2.pdf"
        )
    ]
    mock_result = MagicMock() # not AsyncMock since session.execute(statement)
    mock_result.all.return_value = mock_results

    mock_session.execute.return_value = mock_result

    return mock_session

@pytest.fixture(scope="function")
async def async_client(mock_async_session):
    """Override the dependency for generating an async session with the mock."""
    app.dependency_overrides[generate_async_session] = lambda: mock_async_session
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
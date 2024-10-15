import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
import os
import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI
from httpx import AsyncClient
from core.server import app
from core.config import config
from core.database.session import generate_async_session
from app.controllers.insurance import get_all_policies_async
from sqlalchemy import Row
from app.models.responses.insurance import InsuranceResponse
import logging
@pytest.fixture
def mock_async_session():
    mock_session = AsyncMock(spec=AsyncSession)

    # Create mock results that match the select statement
    mock_results = [
        (101, "https://example.com/policy1.pdf", 1),
        (102, "https://example.com/policy2.pdf", 2)
    ]

    # Create a mock result
    mock_result = AsyncMock()
    mock_result.all.return_value = mock_results

    # # Configure execute to return the mock_result
    async def async_execute(stmt):
        print(f"Mock execute called with statement: {stmt}")
        return mock_result

    mock_session.execute = async_execute

    return mock_session
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_get_all_policies_async(mock_async_session):
    try:
        print("Test function started")
        result = await get_all_policies_async(mock_async_session, customer_id=1)
        print(f"Result type: {type(result)}")
        print(f"Result content: {result}")

        assert result is not None, "Result is None"
        assert isinstance(result, list), f"Expected list, got {type(result)}"
        assert len(result) == 2, f"Expected 2 items, got {len(result)}"

        for i, item in enumerate(result):
            print(f"Item {i}: {item}")
            assert len(item) == 3, f"Expected tuple of length 3, got {len(item)}"
            assert isinstance(item[0], int), f"Expected int for insurance_id, got {type(item[0])}"
            assert isinstance(item[1], str), f"Expected str for customer_policy_url, got {type(item[1])}"
            assert isinstance(item[2], int), f"Expected int for customer_id, got {type(item[2])}"

        assert result[0][0] == 101, f"Expected insurance_id 101, got {result[0][0]}"
        assert result[1][0] == 102, f"Expected insurance_id 102, got {result[1][0]}"
        assert result[0][1] == "https://example.com/policy1.pdf", f"Unexpected customer_policy_url: {result[0][1]}"
        assert result[1][1] == "https://example.com/policy2.pdf", f"Unexpected customer_policy_url: {result[1][1]}"
        assert result[0][2] == 1, f"Expected customer_id 1, got {result[0][2]}"
        assert result[1][2] == 2, f"Expected customer_id 2, got {result[1][2]}"

        print("All assertions passed")
    except Exception as e:
        print(f"Unexpected exception: {type(e).__name__} - {str(e)}")
        raise
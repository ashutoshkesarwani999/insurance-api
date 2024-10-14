import os
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, patch
from api.v1.insurances.insurances import insurance_router  # Adjust the import according to your structure
from app.models.responses.insurance import InsuranceResponse

# Create a FastAPI app and include the router for testing
app = FastAPI()
app.include_router(insurance_router)

# Sample insurance data for testing
mock_insurance_data = [
    {
        "insurance_id": 1,
        "customer_policy_url": "https://example.com/policy1.pdf",
        "customer_id": 123,
    },
    {
        "insurance_id": 2,
        "customer_policy_url": "https://example.com/policy2.pdf",
        "customer_id": 123,
    },
]

@pytest.mark.asyncio
async def test_get_insurances():
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)

    # Mock the get_all_policies_async function to return the mock data
    with patch('app.controllers.insurance.get_all_policies_async', return_value=mock_insurance_data):
        client = TestClient(app)

        # Act
        response = client.get("/123")  # Test with customer_id = 123

    # Assert
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_insurances_no_data_found():
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)

    # Mock the get_all_policies_async function to return an empty list
    with patch('app.controllers.insurance.get_all_policies_async', return_value=[]):
        client = TestClient(app)

        # Act
        response = client.get("/123")  # Test with customer_id = 123

    # Assert
    assert response.status_code == 200

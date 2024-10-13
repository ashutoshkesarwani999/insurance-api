from fastapi import APIRouter, Depends, Request

from app.models.responses.insurance import (
    InsuranceResponse,
    sampleInsuranceResponse,
    sampleListInsuranceResponse,
)

insurance_router = APIRouter()


@insurance_router.get(
    "/",
    response_model=list[InsuranceResponse],
    summary="Retrieve all insurances",
    description="Fetch a list of all available insurances.",
    tags=["Insurance"],
    responses=sampleListInsuranceResponse,
)
async def get_insurances(request: Request) -> list[InsuranceResponse]:
    print("request", request)
    return [
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


@insurance_router.get(
    "/{id}",
    response_model=InsuranceResponse,
    summary="Retrieve a specific insurance",
    description="Fetch details of a specific insurance by its UUID.",
    tags=["Insurance"],
    responses=sampleInsuranceResponse,
)
async def get_insurance(
    id: int,
) -> InsuranceResponse:
    return {
        "policy_name": "Policy 2",
        "policy_url": "https://example.com/policy2",
        "policy_id": 2,
    }

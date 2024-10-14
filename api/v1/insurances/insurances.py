from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from core.database.session import generate_async_session
from app.controllers.insurance import get_all_policies_async, get_one_policy_async
from app.models.responses.insurance import (
    InsuranceResponse,
    sampleInsuranceResponse,
    sampleListInsuranceResponse,
)
from app.logger.logger import logger
from app.service.presigned_url import generate_presigned_url

insurance_router = APIRouter()


@insurance_router.get(
    "/{customer_id}",
    response_model=List[InsuranceResponse],
    summary="Retrieve all insurances",
    description="Fetch a list of all available insurances.",
    tags=["Insurance"],
    responses=sampleListInsuranceResponse,
)
async def get_insurances(
    customer_id: int, async_session: AsyncSession = Depends(generate_async_session)
) -> List[InsuranceResponse]:
    try:
        insurance_list: List[InsuranceResponse] = await get_all_policies_async(
            async_session=async_session, customer_id=customer_id
        )

        if not insurance_list:
            raise HTTPException(status_code=404, detail="Insurance not found")

        processed_insurance_list = [
            InsuranceResponse(
                insurance_id=insurance.insurance_id,
                customer_policy_url=generate_presigned_url(
                    insurance.customer_policy_url
                ),
                customer_id=insurance.customer_id,
            )
            for insurance in insurance_list
        ]
        return processed_insurance_list
    except ValueError as e:
        logger.warning(str(e), exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        logger.warning(f"HTTPException occurred: {e.detail}", exc_info=False)
        raise e
    except Exception as e:
        logger.error(str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@insurance_router.get(
    "/get_policy/{customer_id}/{insurance_id}",
    response_model=InsuranceResponse | dict,
    summary="Retrieve a specific insurance",
    description="Fetch details of a specific insurance by its UUID.",
    tags=["Insurance"],
    responses=sampleInsuranceResponse,
)
async def get_insurance(
    customer_id: int,
    insurance_id: int,
    async_session: AsyncSession = Depends(generate_async_session),
) -> InsuranceResponse:
    try:
        insurance = await get_one_policy_async(
            async_session=async_session,
            insurance_id=int(insurance_id),
            customer_id=int(customer_id),
        )
        if not insurance:
            raise HTTPException(status_code=404, detail="Insurance not found")
        processed_insurance = InsuranceResponse(
            insurance_id=insurance.insurance_id,
            customer_policy_url=generate_presigned_url(insurance.customer_policy_url),
            customer_id=insurance.customer_id,
        )
        return processed_insurance

    except ValueError as e:
        logger.warning(str(e), exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))

    except HTTPException as e:
        logger.warning(f"HTTPException occurred: {e.detail}", exc_info=False)
        raise e
    except Exception as e:
        logger.error(str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

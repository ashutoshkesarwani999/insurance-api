import os
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
    """
    Retrieve all insurance policies for a given customer.

    ### Args:
        customer_id (int): The ID of the customer whose insurance policies are to be retrieved.
        async_session (AsyncSession): The asynchronous database session, injected by FastAPI.

    ### Returns:
        List[InsuranceResponse]: A list of InsuranceResponse objects, each representing an insurance policy.

    ### Raises:
        HTTPException:
            - 404 if no insurance policies are found for the given customer.
            - 400 for any ValueError that occurs during processing.
            - 500 for any unexpected errors.

    ### Example:
        GET /insurances/123
    """
    try:
        insurance_list: List[InsuranceResponse] = await get_all_policies_async(
            async_session=async_session, customer_id=customer_id
        )

        if not insurance_list:
            raise HTTPException(status_code=404, detail="Insurance not found")
        print(insurance_list)
        if os.getenv("AWS_ACCESS_KEY_ID") and not os.getenv("AWS_SECRET_ACCESS_KEY"):
            return insurance_list
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
    """
    Retrieve a specific insurance policy for a given customer.
    ### Args:
        customer_id (int): The ID of the customer.
        insurance_id (int): The ID of the insurance policy.
        async_session (AsyncSession): The asynchronous database session.

    ### Returns:
        Union[InsuranceResponse, dict]: The processed insurance data as an InsuranceResponse object,
                                        or a dictionary containing the raw insurance data.

    ### Raises:
        HTTPException:
            - 404 if the insurance policy is not found.
            - 400 for any ValueError that occurs during processing.
            - 500 for any unexpected errors.

    ### Example:
        insurance = await get_insurance(customer_id=1, insurance_id=100, async_session=session)
    """
    try:
        insurance = await get_one_policy_async(
            async_session=async_session,
            insurance_id=int(insurance_id),
            customer_id=int(customer_id),
        )
        if not insurance:
            raise HTTPException(status_code=404, detail="Insurance not found")

        if os.getenv("AWS_ACCESS_KEY_ID") and not os.getenv("AWS_SECRET_ACCESS_KEY"):
            return insurance

        print(insurance)
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

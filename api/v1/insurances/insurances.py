import json
import redis
from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.session import generate_async_session
from core.cache.redis import get_redis_client
from app.controllers.insurance import get_all_policies_async, get_one_policy_async
from app.models.requests.insurance import RequestModel
from app.models.responses.insurance import (
    InsuranceResponse,
    sampleInsuranceResponse,
    sampleListInsuranceResponse,
)
from app.logger.logger import logger

insurance_router = APIRouter()


@insurance_router.get(
    "/{customer_id}",
    response_model=list[InsuranceResponse],
    summary="Retrieve all insurances",
    description="Fetch a list of all available insurances.",
    tags=["Insurance"],
    responses=sampleListInsuranceResponse,
)
async def get_insurances(
    customer_id: RequestModel,
    async_session: AsyncSession = Depends(generate_async_session),
    redis: redis = Depends(get_redis_client),
) -> list[InsuranceResponse]:
        cache_key = f"all_policies:{customer_id}"

        # Try to get data from cache
        cached_data = redis.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for all policies of customer {customer_id}")
            return json.loads(cached_data)
        insurance = await get_all_policies_async(
            async_session=async_session,
            customer_id=customer_id
        )

        redis.setex(cache_key, 3600, json.dumps([ins.dict() for ins in insurance]))
        return insurance


@insurance_router.get(
    "/get_policy/{customer_id}/{insurance_id}",
    response_model=InsuranceResponse|dict,
    summary="Retrieve a specific insurance",
    description="Fetch details of a specific insurance by its UUID.",
    tags=["Insurance"],
    responses=sampleInsuranceResponse,
)
async def get_insurance(
    customer_id: RequestModel, insurance_id: RequestModel,
    async_session: AsyncSession = Depends(generate_async_session),
    redis: redis = Depends(get_redis_client)
) -> InsuranceResponse|dict:
    cache_key = f"policy:{customer_id}:{insurance_id}"

    cached_data = redis.get(cache_key)
    if cached_data:
        logger.info(f"Cache hit for policy {insurance_id} of customer {customer_id}")
        return json.loads(cached_data)

    insurance = await get_one_policy_async(
        async_session=async_session,
        insurance_id=int(insurance_id),
        customer_id=int(customer_id)
    )
    redis.setex(cache_key, 3600, json.dumps(insurance.dict() if isinstance(insurance, InsuranceResponse) else insurance))
    return insurance


@insurance_router.post(
    "/invalidate_cache",
    summary="Invalidate cache for a customer",
    description="Invalidate all cached data for a specific customer.",
    tags=["Insurance"])
async def invalidate_cache(
    customer_id: str,
    redis: redis = Depends(get_redis_client),
):
    redis.delete(f"all_policies:{customer_id}")

    for key in redis.scan_iter(f"policy:{customer_id}:*"):
        redis.delete(key)

    return {"message": f"Cache invalidated for customer {customer_id}"}
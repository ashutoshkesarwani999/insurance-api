
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, NoResultFound, MultipleResultsFound
from fastapi import HTTPException

from app.schemas.insurance import Insurance

from app.logger.logger import logger

async def get_all_policies_async(async_session: AsyncSession, customer_id: int = None):
    """
    Retrieves a list of policies from the database, optionally filtered by insurance_id and customer_id.

    Args:
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.
        insurance_id (str, optional): The ID of the insurance to filter by.
        customer_id (str, optional): The ID of the customer to filter by.

    Returns:
        A list of dictionaries containing insurance_id, customer_policy_url, and customer_id.
    """
    statement = select(Insurance.insurance_id, Insurance.customer_policy_url, Insurance.customer_id)
    if customer_id is not None:
        statement = statement.where(Insurance.customer_id == customer_id)

    try:
        result = await async_session.execute(statement)
        insurances = result.all()
        if not insurances:
            raise HTTPException(status_code=200,detail="No records found")
        return insurances
    except SQLAlchemyError as e:
        logger.error(f"Unexpected error in get_insurance_route: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


async def get_one_policy_async(async_session: AsyncSession, insurance_id: str = None, customer_id: str = None):

    """
    Retrieves a single insurance from the database by insurance_id and customer_id.

    Args:
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.
        insurance_id (str): The ID of the insurance to retrieve.
        customer_id (str): The ID of the customer associated with the insurance.

    Returns:
        A dictionary containing insurance_id, customer_policy_url, and customer_id if found, None otherwise.
    """
    statement = select(Insurance.insurance_id, Insurance.customer_policy_url, Insurance.customer_id)
    if customer_id is not None and insurance_id is not None:
        statement = statement.where(Insurance.insurance_id == insurance_id, Insurance.customer_id == customer_id)


    try:
        result = await async_session.execute(statement)
        insurance = result.first()
        if insurance:
            return insurance
        return {}
    except SQLAlchemyError as e:
        logger.error(f"Unexpected error in get_insurance_route: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

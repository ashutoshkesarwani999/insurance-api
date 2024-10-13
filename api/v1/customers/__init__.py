from fastapi import APIRouter

from .customers import customer_router

customers_router = APIRouter()
customers_router.include_router(customer_router, tags=["customers"])

__all__ = ["customers_router"]

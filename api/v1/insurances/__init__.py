from fastapi import APIRouter

from .insurances import insurance_router

insurance_routers = APIRouter()
insurance_routers.include_router(
    insurance_router,
    tags=["Insurances"],
)
__all__ = ["insurance_routers"]

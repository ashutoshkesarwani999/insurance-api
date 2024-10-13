from fastapi import APIRouter, Depends

from core.fastapi.dependencies.authentication import AuthenticationRequired

from .insurances import insurance_router

insurance_routers = APIRouter()
insurance_routers.include_router(
    insurance_router,
    tags=["Insurances"],
    dependencies=[Depends(AuthenticationRequired)],
)

__all__ = ["insurance_routers"]

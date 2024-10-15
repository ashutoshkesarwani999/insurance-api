from fastapi import APIRouter
from .health import health_router
from .insurances import insurance_router
# from .customers import customers_router

v1_router = APIRouter()
v1_router.include_router(insurance_router, prefix="/insurance")
v1_router.include_router(health_router, prefix="/health")

# v1_router.include_router(customers_router, prefix="/customer")

from fastapi import APIRouter, Depends, Body

from core.database.session import test_connection
from app.logger.logger import logger

health_router = APIRouter()

@health_router.get("/")
async def health_check():
    db_connected = await test_connection()
    return {
        "status": "healthy" if db_connected else "unhealthy",
        "database_connected": db_connected
    }

from fastapi import APIRouter, Depends, status
import asyncio

from app.models.extras.token import Token
from app.models.requests.customers import LoginCustomerRequest, RegisterUserRequest
from app.models.responses.customers import CustomerRegistrationResponse,sampleResponses
from app.models.extras.token import Token, sampleLoginResponse

customer_router = APIRouter()


@customer_router.post(
        "/register",
        status_code=status.HTTP_201_CREATED,
        response_model=CustomerRegistrationResponse,
        summary="Create a Insurance user",
        responses=sampleResponses,
        tags=["Customer"])
async def register_customer(
    register_customer_request: RegisterUserRequest,
) -> CustomerRegistrationResponse:
    return {
        "customer_id": 123,
        "email": "test@example.com",
        "username": "testuser"
    }


@customer_router.post("/login",
                  response_model=Token,
                  summary="Validates and Retrieves JWT Token of the user",
                  status_code=status.HTTP_200_OK,
                  responses=sampleLoginResponse,
        tags=["Customer"])
async def login_user(
    login_customer_request: LoginCustomerRequest,
) -> Token:
    return Token(
        access_token="fake_access_token",
        refresh_token="fake_refresh_token",
        expires_in= 3600,
        type="Bearer"
    )

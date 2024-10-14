from fastapi import APIRouter, Depends, status
from app.controllers.auth import AuthController
from app.models.requests.customers import LoginCustomerRequest, RegisterUserRequest
from app.models.responses.customers import CustomerRegistrationResponse, sampleResponses
from app.models.extras.token import Token, sampleLoginResponse
from core.factory.factory import Factory

customer_router = APIRouter()


@customer_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=CustomerRegistrationResponse,
    summary="Create a Insurance user",
    responses=sampleResponses,
    tags=["Customer"],
)
async def register_customer(
    register_customer_request: RegisterUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller)
) -> CustomerRegistrationResponse:
    return await auth_controller.register(
        email=register_customer_request.email,
        password=register_customer_request.password,
        username=register_customer_request.username,
    )


@customer_router.post(
    "/login",
    response_model=Token,
    summary="Validates and Retrieves JWT Token of the user",
    status_code=status.HTTP_200_OK,
    responses=sampleLoginResponse,
    tags=["Customer"],
)
async def login_user(
    login_customer_request: LoginCustomerRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),

) -> Token:
    return await auth_controller.login(
        email=login_customer_request.email, password=login_customer_request.password
    )
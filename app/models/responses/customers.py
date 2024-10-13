from pydantic import UUID4, BaseModel, Field
from typing_extensions import Annotated

class CustomerRegistrationResponse(BaseModel):
    email: Annotated[str, Field(example="john.doe@example.com")]
    username: Annotated[str, Field(example="john.doe")]
    customer_id: Annotated[int, Field(example=1234)]

    class Config:
        orm_mode = True

sampleResponses = {
        201: {
            "description": "User successfully created",
            "content": {
                "application/json": {
                    "example": {
                        "customer_id": 1234,
                        "email": "john.doe@example.com",
                        "username": "john.doe"
                    }
                }
            }
        },
        400: {
            "description": "Invalid input",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid email or username"
                    }
                }
            }
        }
    }
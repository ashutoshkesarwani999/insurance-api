from pydantic import BaseModel, Field
from typing_extensions import Annotated

class Token(BaseModel):
    access_token: Annotated[str, Field(example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")]
    refresh_token: Annotated[str, Field(example="dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4")]

sampleLoginResponse = {
    200: {
        "description": "Successful login",
        "content": {
            "application/json": {
                "example": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
                    "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4",
                }
            }
        },
    },
    400: {
        "description": "Invalid credentials",
        "content": {
            "application/json": {"example": {"detail": "Invalid email or password"}}
        },
    },
    401: {
        "description": "Unauthorized",
        "content": {"application/json": {"example": {"detail": "Unauthorized access"}}},
    },
}

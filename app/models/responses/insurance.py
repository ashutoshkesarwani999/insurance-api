from pydantic import BaseModel, Field
from typing_extensions import Annotated

class InsuranceResponse(BaseModel):
    customer_id: Annotated[int, Field(..., description="Policy ID", example="1")]
    customer_policy_url: Annotated[
        str, Field(..., description="Policy URL", example="https://example.com/policy1")
    ]
    insurance_id: Annotated[
        int,
        Field(
            ..., description="Insurance ID", example=1
        ),
    ]

    class Config:
        orm_mode = True

sampleListInsuranceResponse = {
    200: {
        "description": "List of policies retrieved successfully",
        "content": {
            "application/json": {
                "example": [
                    {
                        "customer_id": 1,
                        "customer_policy_url": "https://example.com/policy1",
                        "insurance_id": 1,
                    },
                    {
                        "customer_id": 2,
                        "customer_policy_url": "https://example.com/policy2",
                        "insurance_id": 2,
                    },
                ]
            }
        },
    }
}

sampleInsuranceResponse = {
    200: {
        "description": "Policy details retrieved successfully",
        "content": {
            "application/json": {
                "example": {
                    "customer_id": 1,
                    "customer_policy_url": "https://example.com/policy1",
                    "insurance_id": 1,
                }
            }
        },
    },
    404: {
        "description": "Policy not found",
        "content": {"application/json": {"example": {"detail": "Policy not found"}}},
    },
}

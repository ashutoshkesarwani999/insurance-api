from datetime import date
from pydantic import BaseModel, Field
from typing_extensions import Annotated

class CustomerInsurance(BaseModel):
    customer_policy_id: Annotated[int, Field(..., description="Primary key of the customer policy")]
    customer_id: Annotated[int, Field(..., description="Foreign key referencing the customer")]
    policy_id: Annotated[int, Field(..., description="Foreign key referencing the policy")]
    customer_policy_url: Annotated[str, Field(..., description="URL of the customer policy")]
    created_at: Annotated[date, Field(..., description="Creation date of the customer policy")]
    updated_at: Annotated[date, Field(..., description="Last update date of the customer policy")]

    class Config:
        schema_extra = {
            "example": {
                "customer_policy_id": 1,
                "customer_id": 123,
                "policy_id": 456,
                "customer_policy_url": "http://example.com/policy/123",
                "created_at": "2023-01-01",
                "updated_at": "2023-01-02"
            }
        }
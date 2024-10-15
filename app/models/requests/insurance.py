from datetime import date
from pydantic import BaseModel, Field,model_validator
from typing import Optional

from typing_extensions import Annotated

class CustomerInsurance(BaseModel):
    customer_insurance_id: Annotated[int, Field(..., description="Primary key of the customer policy")]
    customer_id: Annotated[int, Field(..., description="Foreign key referencing the customer")]
    insurance_id: Annotated[int, Field(..., description="Foreign key referencing the policy")]
    customer_policy_url: Annotated[str, Field(..., description="URL of the customer policy")]
    created_at: Annotated[date, Field(..., description="Creation date of the customer policy")]
    updated_at: Annotated[date, Field(..., description="Last update date of the customer policy")]

    class Config:
        schema_extra = {
            "example": {
                "customer_insurance_id": 1,
                "customer_id": 123,
                "insurance_id": 456,
                "customer_policy_url": "http://example.com/policy/123",
                "created_at": "2023-01-01",
                "updated_at": "2023-01-02"
            }
        }

class RequestModel(BaseModel):
    customer_id: Annotated[Optional[int], Field(None, description="ID of the customer")] = None
    insurance_id: Annotated[Optional[int], Field(None, description="ID of the policy")] = None

    @model_validator(mode='after')
    def check_at_least_one_field(cls, values):
        if values.get('customer_id') is None and values.get('insurance_id') is None:
            raise ValueError("At least one of customer_id or insurance_id must be provided")
        return values

    class Config:
        schema_extra = {
            "example": {
                "customer_id": 123,
                "insurance_id": 456,
            }
        }

from pydantic import BaseModel, Field


class CurrentCustomer(BaseModel):
    customer_id: int = Field(None, description="Customer ID")

    class Config:
        validate_assignment = True

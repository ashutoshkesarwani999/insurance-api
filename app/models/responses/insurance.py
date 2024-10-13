from pydantic import UUID4, BaseModel, Field
from typing_extensions import Annotated


class InsuranceResponse(BaseModel):
    title: Annotated[str, Field(..., description="Task name", example="Task 1")]
    description: Annotated[
        str, Field(..., description="Task description", example="Task 1 description")
    ]
    completed: Annotated[
        bool, Field(alias="is_completed", description="Task completed status")
    ]
    uuid: Annotated[
        UUID4,
        Field(
            ..., description="Task UUID", example="a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
        ),
    ]

    class Config:
        orm_mode = True


sampleListInsuranceResponse = {
    200: {
        "description": "List of insurances retrieved successfully",
        "content": {
            "application/json": {
                "example": [
                    {
                        "title": "Insurance 1",
                        "description": "Description of Insurance 1",
                        "completed": False,
                        "uuid": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                    },
                    {
                        "title": "Insurance 2",
                        "description": "Description of Insurance 2",
                        "completed": True,
                        "uuid": "b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12",
                    },
                ]
            }
        },
    }
}
sampleInsuranceResponse = {
    200: {
        "description": "Insurance details retrieved successfully",
        "content": {
            "application/json": {
                "example": {
                    "title": "Insurance 1",
                    "description": "Description of Insurance 1",
                    "completed": False,
                    "uuid": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                }
            }
        },
    },
    404: {
        "description": "Insurance not found",
        "content": {"application/json": {"example": {"detail": "Insurance not found"}}},
    },
}

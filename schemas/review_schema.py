from datetime import datetime

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):

    customer_id: int

    package_id: int

    booking_id: int

    rating: int = Field(
        ge=1,
        le=5
    )

    review_text: str = Field(
        min_length=1
    )


class ReviewUpdate(BaseModel):

    rating: int = Field(
        ge=1,
        le=5
    )

    review_text: str = Field(
        min_length=1
    )


class ReviewResponse(BaseModel):

    id: int

    customer_id: int

    package_id: int

    booking_id: int

    rating: int

    review_text: str

    created_at: datetime

    class Config:
        from_attributes = True
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class BookingCreate(BaseModel):

    customer_id: int = Field(
        gt=0
    )

    package_id: int = Field(
        gt=0
    )

    number_of_travelers: int = Field(
        gt=0
    )

    discount: float = Field(
        default=0,
        ge=0
    )

    tax: float = Field(
        default=0,
        ge=0
    )


class BookingResponse(BaseModel):

    id: int
    customer_id: int
    package_id: int
    booking_date: date
    number_of_travelers: int
    base_amount: float
    discount: float
    tax: float
    total_amount: float
    booking_status: str

    class Config:
        from_attributes = True
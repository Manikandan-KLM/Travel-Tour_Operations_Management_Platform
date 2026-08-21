from datetime import datetime

from pydantic import BaseModel, Field


class CancellationCreate(BaseModel):

    cancellation_reason: str = Field(
        min_length=3
    )


class CancellationResponse(BaseModel):

    id: int

    booking_id: int

    cancellation_reason: str

    cancellation_date: datetime

    refund_percentage: float

    refund_amount: float

    class Config:
        from_attributes = True
from datetime import datetime

from pydantic import BaseModel, Field


class PaymentCreate(BaseModel):

    amount: float = Field(gt=0)

    payment_method: str

    transaction_id: str


class PaymentResponse(BaseModel):

    id: int

    booking_id: int

    amount: float

    payment_method: str

    transaction_id: str

    payment_status: str

    payment_date: datetime

    class Config:
        from_attributes = True
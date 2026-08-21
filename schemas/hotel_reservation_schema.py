from datetime import date

from pydantic import BaseModel, Field


class HotelReservationCreate(BaseModel):

    booking_id: int = Field(
        gt=0
    )

    room_id: int = Field(
        gt=0
    )

    check_in: date

    check_out: date

    number_of_rooms: int = Field(
        gt=0
    )


class HotelReservationResponse(BaseModel):

    id: int
    booking_id: int
    room_id: int
    check_in: date
    check_out: date
    number_of_rooms: int
    total_amount: float

    class Config:
        from_attributes = True
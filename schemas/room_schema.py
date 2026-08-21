from pydantic import BaseModel, Field


class RoomCreate(BaseModel):

    hotel_id: int = Field(
        gt=0
    )

    room_type: str

    room_number: str

    price_per_night: float = Field(
        gt=0
    )

    capacity: int = Field(
        gt=0
    )

    availability_status: str = "Available"


class RoomResponse(BaseModel):

    id: int
    hotel_id: int
    room_type: str
    room_number: str
    price_per_night: float
    capacity: int
    availability_status: str

    class Config:
        from_attributes = True
from pydantic import BaseModel, Field


class HotelCreate(BaseModel):

    hotel_name: str

    destination_id: int = Field(
        gt=0
    )

    address: str

    rating: float = Field(
        default=0,
        ge=0,
        le=5
    )

    contact_number: str


class HotelResponse(BaseModel):

    id: int
    hotel_name: str
    destination_id: int
    address: str
    rating: float
    contact_number: str

    class Config:
        from_attributes = True
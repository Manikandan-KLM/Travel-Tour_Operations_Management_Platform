from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class TravelerCreate(BaseModel):

    full_name: str = Field(
        min_length=2,
        max_length=150
    )

    date_of_birth: date

    gender: str = Field(
        min_length=1,
        max_length=20
    )

    passport_number: Optional[str] = Field(
        default=None,
        max_length=50
    )

    nationality: str = Field(
        min_length=2,
        max_length=100
    )

    special_requirements: Optional[str] = Field(
        default=None,
        max_length=500
    )


class TravelerUpdate(BaseModel):

    full_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    date_of_birth: Optional[date] = None

    gender: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=20
    )

    passport_number: Optional[str] = Field(
        default=None,
        max_length=50
    )

    nationality: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    special_requirements: Optional[str] = Field(
        default=None,
        max_length=500
    )


class TravelerResponse(BaseModel):

    id: int
    booking_id: int
    full_name: str
    date_of_birth: date
    gender: str
    passport_number: Optional[str]
    nationality: str
    special_requirements: Optional[str]

    class Config:
        from_attributes = True
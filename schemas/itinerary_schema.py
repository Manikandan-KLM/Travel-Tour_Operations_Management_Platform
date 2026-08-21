from datetime import time
from typing import Optional

from pydantic import BaseModel, Field


class ItineraryCreate(BaseModel):

    day_number: int = Field(
        gt=0
    )

    title: str = Field(
        min_length=2,
        max_length=150
    )

    description: Optional[str] = None

    location: str = Field(
        min_length=2,
        max_length=150
    )

    start_time: time

    end_time: time


class ItineraryUpdate(BaseModel):

    day_number: Optional[int] = Field(
        default=None,
        gt=0
    )

    title: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    description: Optional[str] = None

    location: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    start_time: Optional[time] = None

    end_time: Optional[time] = None


class ItineraryResponse(BaseModel):

    id: int
    package_id: int
    day_number: int
    title: str
    description: Optional[str]
    location: str
    start_time: time
    end_time: time

    class Config:
        from_attributes = True
from datetime import datetime

from pydantic import BaseModel, Field


class ActivityCreate(BaseModel):

    package_id: int

    activity_name: str

    location: str

    duration: int = Field(gt=0)

    price: float = Field(gt=0)

    capacity: int = Field(gt=0)

    start_time: datetime

    end_time: datetime


class ActivityResponse(BaseModel):

    id: int

    package_id: int

    activity_name: str

    location: str

    duration: int

    price: float

    capacity: int

    start_time: datetime

    end_time: datetime

    guide_id: int | None = None

    class Config:
        from_attributes = True
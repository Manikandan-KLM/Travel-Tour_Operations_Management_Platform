from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


PACKAGE_STATUSES = {
    "Draft",
    "Published",
    "Full",
    "Completed",
    "Cancelled"
}


class PackageCreate(BaseModel):

    package_name: str = Field(min_length=2,max_length=150)

    destination_id: int = Field(gt=0)

    description: Optional[str] = None

    duration_days: int = Field(gt=0)

    base_price: float = Field(gt=0)

    max_capacity: int = Field(gt=0)

    available_slots: int = Field(ge=0)

    start_date: date

    end_date: date

    status: str = "Draft"


class PackageUpdate(BaseModel):

    package_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    destination_id: Optional[int] = Field(
        default=None,
        gt=0
    )

    description: Optional[str] = None

    duration_days: Optional[int] = Field(
        default=None,
        gt=0
    )

    base_price: Optional[float] = Field(
        default=None,
        gt=0
    )

    max_capacity: Optional[int] = Field(
        default=None,
        gt=0
    )

    available_slots: Optional[int] = Field(
        default=None,
        ge=0
    )

    start_date: Optional[date] = None

    end_date: Optional[date] = None

    status: Optional[str] = None


class PackageResponse(BaseModel):

    id: int
    package_name: str
    destination_id: int
    description: Optional[str]
    duration_days: int
    base_price: float
    max_capacity: int
    available_slots: int
    start_date: date
    end_date: date
    status: str

    class Config:
        from_attributes = True


class PackageListResponse(BaseModel):

    total: int
    page: int
    limit: int
    total_pages: int
    data: list[PackageResponse]
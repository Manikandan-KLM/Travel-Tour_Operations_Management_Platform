from typing import Optional

from pydantic import BaseModel, Field


class DestinationCreate(BaseModel):

    name: str = Field(min_length=2,max_length=100)

    country: str = Field(min_length=2,max_length=100)

    state: str = Field(min_length=2,max_length=100)

    description: Optional[str] = None

    best_season: str = Field(min_length=2,max_length=50)

    status: str = "Active"


class DestinationUpdate(BaseModel):

    name: Optional[str] = Field(default=None,min_length=2,max_length=100)

    country: Optional[str] = Field(default=None,min_length=2,max_length=100)

    state: Optional[str] = Field(default=None,min_length=2,max_length=100)

    description: Optional[str] = None

    best_season: Optional[str] = Field(default=None,min_length=2,max_length=50)

    status: Optional[str] = None


class DestinationResponse(BaseModel):

    id: int
    name: str
    country: str
    state: str
    description: Optional[str]
    best_season: str
    status: str

    class Config:
        from_attributes = True
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class CustomerCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=150
    )

    email: EmailStr

    phone: str = Field(
        min_length=7,
        max_length=20
    )

    address: Optional[str] = Field(
        default=None,
        max_length=300
    )

    emergency_contact: Optional[str] = Field(
        default=None,
        max_length=20
    )


class CustomerUpdate(BaseModel):

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    email: Optional[EmailStr] = None

    phone: Optional[str] = Field(
        default=None,
        min_length=7,
        max_length=20
    )

    address: Optional[str] = Field(
        default=None,
        max_length=300
    )

    emergency_contact: Optional[str] = Field(
        default=None,
        max_length=20
    )


class CustomerResponse(BaseModel):

    id: int
    name: str
    email: str
    phone: str
    address: Optional[str]
    emergency_contact: Optional[str]

    class Config:
        from_attributes = True
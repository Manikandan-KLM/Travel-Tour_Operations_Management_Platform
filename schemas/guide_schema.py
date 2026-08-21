from pydantic import BaseModel, EmailStr


class GuideCreate(BaseModel):

    name: str

    email: EmailStr

    phone: str

    specialization: str

    availability_status: str = "Active"


class GuideResponse(BaseModel):

    id: int

    name: str

    email: EmailStr

    phone: str

    specialization: str

    availability_status: str

    class Config:
        from_attributes = True
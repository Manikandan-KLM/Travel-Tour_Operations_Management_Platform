from pydantic import BaseModel, EmailStr, Field

from models.user_model import UserRole


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=100
    )


class LoginRequest(BaseModel):
    email: EmailStr

    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True


class ChangePasswordRequest(BaseModel):
    current_password: str

    new_password: str = Field(
        min_length=8,
        max_length=100
    )
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user
from database import get_db

from schemas.auth_schema import (
    ChangePasswordRequest,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse
)

from services.auth_service import auth_service

from utils.rate_limit import limiter


router = APIRouter(prefix="/auth",tags=["Authentication"])

# POST REGISTER ----------------------------------------------------------------

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    return auth_service.register(
        db,
        data
    )

# POST LOGIN --------------------------------------------------------------------

@router.post("/login")
@limiter.limit("5/minute")
def login(

    request: Request,

    user_data: LoginRequest,

    db: Session = Depends(get_db)
):

    return auth_service.login_user(
        db,
        user_data.email,
        user_data.password
    )

# POST REFRESH -----------------------------------------------------------------------

@router.post(
    "/refresh",
    response_model=TokenResponse
)
def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):

    return auth_service.refresh_token(
        db,
        data.refresh_token
    )

# GET ME --------------------------------------------------------------------------

@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user=Depends(get_current_user)
):

    return current_user

# PUT CHANGE PASSWORD -----------------------------------------------------------

@router.put(
    "/change-password",
    response_model=UserResponse
)
def change_password(
    data: ChangePasswordRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return auth_service.change_password(
        db,
        current_user,
        data
    )
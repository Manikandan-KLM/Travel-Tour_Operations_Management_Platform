from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from auth.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password
)

from models.user_model import User, UserRole

from repositories.user_repository import user_repository

from auth.password import hash_password

from schemas.auth_schema import (
    ChangePasswordRequest,
    LoginRequest,
    RegisterRequest
)


class AuthService:

    def register(
        self,
        db: Session,
        data: RegisterRequest
    ):

        existing_user = user_repository.get_by_email(
            db,
            data.email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        user = User(
            full_name=data.full_name,
            email=data.email,
            hashed_password=hash_password(data.password),
            role=UserRole.CUSTOMER.value,
            is_active=True
        )

        return user_repository.create(db, user)

    def login(
        self,
        db: Session,
        data: LoginRequest
    ):

        user = user_repository.get_by_email(
            db,
            data.email
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not verify_password(
            data.password,
            user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated"
            )

        access_token = create_access_token(
            user.id,
            user.role
        )

        refresh_token = create_refresh_token(
            user.id
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    def refresh_token(
        self,
        db: Session,
        refresh_token: str
    ):

        try:
            payload = decode_token(refresh_token)

        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        user = user_repository.get_by_id(
            db,
            int(user_id)
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated"
            )

        access_token = create_access_token(
            user.id,
            user.role
        )

        new_refresh_token = create_refresh_token(
            user.id
        )

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }

    def change_password(
        self,
        db: Session,
        user: User,
        data: ChangePasswordRequest
    ):

        if not verify_password(
            data.current_password,
            user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )

        if data.current_password == data.new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be different"
            )

        user.hashed_password = hash_password(
            data.new_password
        )

        return user_repository.update(db, user)


auth_service = AuthService()
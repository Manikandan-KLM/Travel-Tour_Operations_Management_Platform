from fastapi import HTTPException

from auth.password import (
    verify_password
)

from auth.jwt import (
    create_access_token
)

from repositories import user_repository


def login_user(
    db,
    email,
    password
):

    user = (
        user_repository
        .get_user_by_email(
            db,
            email
        )
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        password,
        user.hashed_password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {
            "sub": str(user.id),
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
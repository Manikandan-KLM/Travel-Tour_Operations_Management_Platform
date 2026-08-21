from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models.user_model import User
from auth.security import decode_token
from database import get_db
from repositories.user_repository import user_repository

from jose import (
    JWTError,
    jwt
)

from config import (
    SECRET_KEY,
    ALGORITHM
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


security = HTTPBearer()


def get_current_user(
    token:str = Depends(
        oauth2_scheme
    ),
    # credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    # token = credentials.credentials

    # try:
    #     payload = decode_token(token)

    # except ValueError:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid or expired access token"
    #     )

    # if payload.get("type") != "access":
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Access token required"
    #     )

    # user_id = payload.get("sub")

    # if not user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid token"
    #     )

    # user = user_repository.get_by_id(
    #     db,
    #     int(user_id)
    # )

    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="User not found"
    #     )

    # if not user.is_active:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Account is deactivated"
    #     )

    # return user


    credentials_exception = HTTPException(

        status_code=status.HTTP_401_UNAUTHORIZED,

        detail="Could not validate credentials",

        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:

            raise credentials_exception

    except JWTError:

        raise credentials_exception

    user = db.query(User).filter(
        User.id == int(user_id),
        User.is_deleted == False
    ).first()

    if not user:

        raise credentials_exception

    return user





# ROLE BASED AUTHORIZATION ---------------------------------------------------------

def require_roles(*allowed_roles):

    def role_checker(
        current_user=Depends(get_current_user)
    ):

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )

        return current_user

    return role_checker

# ADMIN REUIRED --------------------------------------------------------------------

def require_admin(
    current_user = Depends(
        get_current_user
    )
):

    if current_user.role != "Admin":

        raise HTTPException(
            status_code=403,
            detail="Only Admin can access"
        )

    return current_user
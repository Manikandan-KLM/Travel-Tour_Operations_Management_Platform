from fastapi import (
    APIRouter,
    Depends,
    status
)

from sqlalchemy.orm import Session

from database import get_db

from schemas.room_schema import (
    RoomCreate,
    RoomResponse
)

from services.room_service import (
    room_service
)


router = APIRouter(prefix="/rooms",tags=["Rooms"])


@router.post(
    "",
    response_model=RoomResponse,
    status_code=status.HTTP_201_CREATED
)
def create_room(
    data: RoomCreate,
    db: Session = Depends(get_db)
):

    return room_service.create_room(
        db,
        data
    )
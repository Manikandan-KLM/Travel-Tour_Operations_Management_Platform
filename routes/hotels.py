from fastapi import (
    APIRouter,
    Depends,
    status
)

from sqlalchemy.orm import Session

from database import get_db

from schemas.hotel_schema import (
    HotelCreate,
    HotelResponse
)

from services.hotel_service import (
    hotel_service
)

from schemas.room_schema import RoomResponse

from services.room_service import (
    room_service
)

router = APIRouter(prefix="/hotels",tags=["Hotels"])


@router.post(
    "",
    response_model=HotelResponse,
    status_code=status.HTTP_201_CREATED
)
def create_hotel(
    data: HotelCreate,
    db: Session = Depends(get_db)
):

    return hotel_service.create_hotel(
        db,
        data
    )


@router.get(
    "",
    response_model=list[HotelResponse]
)
def get_hotels(
    db: Session = Depends(get_db)
):

    return hotel_service.get_hotels(db)


@router.get(
    "/{hotel_id}/rooms",
    response_model=list[RoomResponse]
)
def get_hotel_rooms(
    hotel_id: int,
    db: Session = Depends(get_db)
):

    return room_service.get_hotel_rooms(
        db,
        hotel_id
    )



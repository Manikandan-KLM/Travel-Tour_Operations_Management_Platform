from fastapi import (
    APIRouter,
    Depends,
    status
)

from sqlalchemy.orm import Session

from database import get_db

from schemas.hotel_reservation_schema import (
    HotelReservationCreate,
    HotelReservationResponse
)

from services.hotel_reservation_service import (
    hotel_reservation_service
)


router = APIRouter(prefix="/hotel-reservations",tags=["Hotel Reservations"])


@router.post(
    "",
    response_model=HotelReservationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_reservation(
    data: HotelReservationCreate,
    db: Session = Depends(get_db)
):

    return (
        hotel_reservation_service
        .create_reservation(
            db,
            data
        )
    )


@router.get(
    "",
    response_model=list[HotelReservationResponse]
)
def get_reservations(
    db: Session = Depends(get_db)
):

    return (
        hotel_reservation_service
        .get_reservations(db)
    )
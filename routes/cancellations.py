from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from database import get_db

from schemas.cancellation_schema import (
    CancellationCreate,
    CancellationResponse
)

from services import cancellation_service


router = APIRouter(prefix="/bookings",tags=["Cancellation"])


@router.post(
    "/{booking_id}/cancel",
    response_model=CancellationResponse
)
def cancel_booking(
    booking_id: int,
    cancellation: CancellationCreate,
    db: Session = Depends(get_db)
):

    return cancellation_service.cancel_booking(
        db=db,
        booking_id=booking_id,
        cancellation_data=cancellation
    )


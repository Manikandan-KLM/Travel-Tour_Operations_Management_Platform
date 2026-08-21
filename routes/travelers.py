from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from auth.dependencies import (
    get_current_user,
    require_roles
)

from database import get_db

from schemas.traveler_schema import (
    TravelerCreate,
    TravelerResponse,
    TravelerUpdate
)

from services.traveler_service import (
    traveler_service
)


router = APIRouter(tags=["Travelers"])

# POST TRAVELERS -----------------------------------------------------------------------------

@router.post(
    "/bookings/{booking_id}/travelers",
    response_model=TravelerResponse,
    status_code=status.HTTP_201_CREATED
)
def create_traveler(
    booking_id: int,
    data: TravelerCreate,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            "Super Admin",
            "Tour Manager",
            "Booking Agent"
        )
    )
):

    return traveler_service.create_traveler(
        db,
        booking_id,
        data
    )

# GET TRAVELERS ----------------------------------------------------------------------------

@router.get(
    "/bookings/{booking_id}/travelers",
    response_model=list[TravelerResponse]
)
def get_booking_travelers(
    booking_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(
        get_current_user
    )
):

    return traveler_service.get_booking_travelers(
        db,
        booking_id
    )

# PUT TRAVELERS -------------------------------------------------------------------

@router.put(
    "/travelers/{traveler_id}",
    response_model=TravelerResponse
)
def update_traveler(
    traveler_id: int,
    data: TravelerUpdate,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            "Super Admin",
            "Tour Manager",
            "Booking Agent"
        )
    )
):

    return traveler_service.update_traveler(
        db,
        traveler_id,
        data
    )
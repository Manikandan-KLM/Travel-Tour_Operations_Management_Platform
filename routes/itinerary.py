from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from auth.dependencies import (
    get_current_user,
    require_roles
)

from database import get_db

from schemas.itinerary_schema import (
    ItineraryCreate,
    ItineraryResponse,
    ItineraryUpdate
)

from services.itinerary_service import (
    itinerary_service
)


router = APIRouter(tags=["Itinerary"])

# POST ITINERARY --------------------------------------------------------------------

@router.post(
    "/packages/{package_id}/itinerary",
    response_model=ItineraryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_itinerary(
    package_id: int,
    data: ItineraryCreate,
    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            "Super Admin",
            "Tour Manager"
        )
    )
):

    return itinerary_service.create_itinerary(
        db,
        package_id,
        data
    )

# GET PACKAGE ITINERARY --------------------------------------------------------------

@router.get(
    "/packages/{package_id}/itinerary",
    response_model=list[ItineraryResponse]
)
def get_package_itinerary(
    package_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(
        get_current_user
    )
):

    return itinerary_service.get_package_itinerary(
        db,
        package_id
    )

# PUT ITINERARY ----------------------------------------------------------------------

@router.put(
    "/itinerary/{itinerary_id}",
    response_model=ItineraryResponse
)
def update_itinerary(
    itinerary_id: int,
    data: ItineraryUpdate,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            "Super Admin",
            "Tour Manager"
        )
    )
):

    return itinerary_service.update_itinerary(
        db,
        itinerary_id,
        data
    )

# DELETE ITINERARY ----------------------------------------------------------------

@router.delete(
    "/itinerary/{itinerary_id}"
)
def delete_itinerary(
    itinerary_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            "Super Admin",
            "Tour Manager"
        )
    )
):

    return itinerary_service.delete_itinerary(
        db,
        itinerary_id
    )
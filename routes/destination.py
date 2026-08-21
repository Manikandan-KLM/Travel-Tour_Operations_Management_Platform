from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from auth.dependencies import (
    get_current_user,
    require_roles
)

from database import get_db

from schemas.destination_schema import (
    DestinationCreate,
    DestinationResponse,
    DestinationUpdate
)

from services.destination_service import (
    destination_service
)


router = APIRouter(prefix="/destinations",tags=["Destinations"])

# POST DESTINATION -------------------------------------------------------------------

@router.post(
    "",
    response_model=DestinationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_destination(
    data: DestinationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "Super Admin",
            "Tour Manager"
        )
    )
):

    return destination_service.create_destination(
        db,
        data
    )

# GET ALL DESTINATION ---------------------------------------------------------------

@router.get(
    "",
    response_model=list[DestinationResponse]
)
def get_destinations(
    search: str | None = Query(
        default=None
    ),

    country: str | None = Query(
        default=None
    ),

    season: str | None = Query(
        default=None
    ),

    page: int = Query(
        default=1,
        ge=1
    ),

    limit: int = Query(
        default=10,
        ge=1,
        le=100
    ),

    db: Session = Depends(get_db),

    current_user=Depends(
        get_current_user
    )
):

    destinations, total = (
        destination_service.get_destinations(
            db=db,
            search=search,
            country=country,
            season=season,
            page=page,
            limit=limit
        )
    )

    return destinations

# GET BY ID DESTINATION -------------------------------------------------------------------

@router.get(
    "/{destination_id}",
    response_model=DestinationResponse
)
def get_destination(
    destination_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    )
):

    return destination_service.get_destination(
        db,
        destination_id
    )

# PUT BY ID DESTINATION -----------------------------------------------------------------

@router.put(
    "/{destination_id}",
    response_model=DestinationResponse
)
def update_destination(
    destination_id: int,
    data: DestinationUpdate,
    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            "Super Admin",
            "Tour Manager"
        )
    )
):

    return destination_service.update_destination(
        db,
        destination_id,
        data
    )

# DELETE BY ID DESTINATION ---------------------------------------------------------

@router.delete(
    "/{destination_id}"
)
def delete_destination(
    destination_id: int,
    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            "Super Admin"
        )
    )
):

    return destination_service.delete_destination(
        db,
        destination_id
    )
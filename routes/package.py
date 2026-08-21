from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from datetime import date

from auth.dependencies import (
    get_current_user,
    require_roles
)

from database import get_db

from schemas.package_schema import (
    PackageCreate,
    PackageListResponse,
    PackageResponse,
    PackageUpdate
)

from services.package_service import (
    package_service
)


router = APIRouter(prefix="/packages",tags=["Tour Packages"])

# POST PACKAGES --------------------------------------------------------------------------

@router.post(
    "",
    response_model=PackageResponse,
    status_code=status.HTTP_201_CREATED
)
def create_package(
    data: PackageCreate,
    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            "Super Admin",
            "Tour Manager"
        )
    )
):

    return package_service.create_package(
        db,
        data
    )

# GET PACKAGES -------------------------------------------------------------------------

@router.get(
    "",
    response_model=PackageListResponse
)
def get_packages(
    search: str | None = Query(
        default=None
    ),

    status_filter: str | None = Query(
        default=None,
        alias="status"
    ),

    destination_id: int | None = Query(
        default=None,
        gt=0
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

    return package_service.get_packages(
        db=db,
        search=search,
        status_filter=status_filter,
        destination_id=destination_id,
        page=page,
        limit=limit
    )

# GET PACKAGES BY ID -----------------------------------------------------------------

@router.get(
    "/{package_id}",
    response_model=PackageResponse
)
def get_package(
    package_id: int,
    db: Session = Depends(get_db),

    current_user=Depends(
        get_current_user
    )
):

    return package_service.get_package(
        db,
        package_id
    )

# PUT PACKAGES BY ID ------------------------------------------------------------------

# @router.put(
#     "/{package_id}",
#     response_model=PackageResponse
# )
# def update_package(
#     package_id: int,
#     data: PackageUpdate,
#     db: Session = Depends(get_db),

#     current_user=Depends(
#         require_roles(
#             "Super Admin",
#             "Tour Manager"
#         )
#     )
# ):

#     return package_service.update_package(
#         db,
#         package_id,
#         data
#     )

@router.put(
    "/{package_id}"
)
def update_package(

    package_id: int,

    package_data: PackageUpdate,

    db: Session = Depends(get_db),

    current_user = Depends(
        require_roles(["Admin"])
    )
):

    return package_service.update_package(

        db=db,

        package_id=package_id,

        package_data=package_data,

        current_user=current_user
    )

# DELETE PACKAGES BY ID ---------------------------------------------------------------

@router.delete(
    "/{package_id}"
)
def delete_package(
    package_id: int,
    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            "Super Admin"
        )
    )
):

    return package_service.delete_package(
        db,
        package_id
    )



@router.get("/search")
def search_packages(

    destination: str | None = None,

    min_price: float | None = None,

    max_price: float | None = None,

    duration: int | None = None,

    package_date: date | None = None,

    availability: bool | None = None,

    min_rating: float | None = None,

    page: int = 1,

    limit: int = 10,

    sort_by: str = "id",

    sort_order: str = "asc",

    db: Session = Depends(get_db)
):

    return package_service.search_packages(

        db=db,

        destination=destination,

        min_price=min_price,

        max_price=max_price,

        duration=duration,

        package_date=package_date,

        availability=availability,

        min_rating=min_rating,

        page=page,

        limit=limit,

        sort_by=sort_by,

        sort_order=sort_order
    )
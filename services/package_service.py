import math
from datetime import date

import json
from cache.redis_client import redis_client

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.package_model import TourPackage

from repositories.destination_repository import (
    destination_repository
)

from repositories.package_repository import (
    package_repository
)

from schemas.package_schema import (
    PACKAGE_STATUSES,
    PackageCreate,
    PackageUpdate
)
from services  import auditlog_service
from repositories import package_repository

class PackageService:

    def create_package(
        self,
        db: Session,
        data: PackageCreate
    ):

        # 1. Validate destination
        destination = destination_repository.get_by_id(
            db,
            data.destination_id
        )

        if not destination:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Destination not found"
            )

        # 2. Validate package name
        existing_package = (
            package_repository.get_by_name(
                db,
                data.package_name
            )
        )

        if existing_package:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Package already exists"
            )

        # 3. Validate status
        if data.status not in PACKAGE_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Invalid package status. "
                    "Allowed: Draft, Published, Full, "
                    "Completed, Cancelled"
                )
            )

        # 4. Validate dates
        if data.end_date <= data.start_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End date must be after start date"
            )

        # 5. Validate capacity
        if data.max_capacity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum capacity must be greater than 0"
            )

        # 6. Validate available slots
        if data.available_slots > data.max_capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Available slots cannot exceed "
                    "maximum capacity"
                )
            )

        # 7. Create package
        package = TourPackage(
            package_name=data.package_name,
            destination_id=data.destination_id,
            description=data.description,
            duration_days=data.duration_days,
            base_price=data.base_price,
            max_capacity=data.max_capacity,
            available_slots=data.available_slots,
            start_date=data.start_date,
            end_date=data.end_date,
            status=data.status
        )

        return package_repository.create(
            db,
            package
        )

    def get_package(
        self,
        db: Session,
        package_id: int
    ):

        package = package_repository.get_by_id(
            db,
            package_id
        )

        if not package:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Package not found"
            )

        return package

    def get_packages(
        self,
        db: Session,
        search: str | None,
        status_filter: str | None,
        destination_id: int | None,
        page: int,
        limit: int
    ):

        packages, total = (
            package_repository.get_all(
                db=db,
                search=search,
                status=status_filter,
                destination_id=destination_id,
                page=page,
                limit=limit
            )
        )

        total_pages = (
            math.ceil(total / limit)
            if total > 0
            else 0
        )

        return {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "data": packages
        }
# -----------------------------------------------------------------------------------------------
    # def update_package(
    #     self,
    #     db: Session,
    #     package_id: int,
    #     data: PackageUpdate
    # ):

    #     package = self.get_package(
    #         db,
    #         package_id
    #     )

    #     update_data = data.model_dump(
    #         exclude_unset=True
    #     )

    #     # ---------------------------------
    #     # Destination validation
    #     # ---------------------------------

    #     if "destination_id" in update_data:

    #         destination = (
    #             destination_repository.get_by_id(
    #                 db,
    #                 update_data["destination_id"]
    #             )
    #         )

    #         if not destination:
    #             raise HTTPException(
    #                 status_code=404,
    #                 detail="Destination not found"
    #             )

    #     # ---------------------------------
    #     # Status validation
    #     # ---------------------------------

    #     if "status" in update_data:

    #         if update_data["status"] not in PACKAGE_STATUSES:
    #             raise HTTPException(
    #                 status_code=400,
    #                 detail="Invalid package status"
    #             )

    #     # ---------------------------------
    #     # Date validation
    #     # ---------------------------------

    #     new_start_date = update_data.get(
    #         "start_date",
    #         package.start_date
    #     )

    #     new_end_date = update_data.get(
    #         "end_date",
    #         package.end_date
    #     )

    #     if new_end_date <= new_start_date:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="End date must be after start date"
    #         )

    #     # ---------------------------------
    #     # Capacity validation
    #     # ---------------------------------

    #     new_max_capacity = update_data.get(
    #         "max_capacity",
    #         package.max_capacity
    #     )

    #     new_available_slots = update_data.get(
    #         "available_slots",
    #         package.available_slots
    #     )

    #     if new_max_capacity <= 0:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="Maximum capacity must be greater than 0"
    #         )

    #     if new_available_slots < 0:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="Available slots cannot be negative"
    #         )

    #     if new_available_slots > new_max_capacity:
    #         raise HTTPException(
    #             status_code=400,
    #             detail=(
    #                 "Available slots cannot exceed "
    #                 "maximum capacity"
    #             )
    #         )

    #     # ---------------------------------
    #     # Update
    #     # ---------------------------------

    #     for field, value in update_data.items():
    #         setattr(
    #             package,
    #             field,
    #             value
    #         )

    #     return package_repository.update(
    #         db,
    #         package
    #     )

def update_package(

    db,

    package_id,

    package_data,

    current_user
):

    package = (
        package_repository
        .get_package_by_id(
            db,
            package_id
        )
    )

    if not package:

        raise HTTPException(
            status_code=404,
            detail="Package not found"
        )

    old_data = {

        "package_name":
            package.package_name,

        "price":
            float(package.price)
    }

    try:

        updated_package = (
            package_repository
            .update_package(

                db,

                package,

                package_data
            )
        )

        new_data = {

            "package_name":
                updated_package.package_name,

            "price":
                float(
                    updated_package.price
                )
        }

        auditlog_service.log_action(

            db=db,

            user_id=current_user.id,

            action="UPDATE",

            entity="Package",

            entity_id=package.id,

            old_data=old_data,

            new_data=new_data
        )

        db.commit()

        db.refresh(updated_package)

        return updated_package

    except Exception:

        db.rollback()

        raise
# -----------------------------------------------------------------------------------------------
    def delete_package(
        self,
        db: Session,
        package_id: int
    ):

        package = self.get_package(
            db,
            package_id
        )

        package_repository.delete(
            db,
            package
        )

        return {
            "message": "Package deleted successfully"
        }



def search_packages(
    db: Session,
    destination=None,
    min_price=None,
    max_price=None,
    duration=None,
    package_date=None,
    availability=None,
    min_rating=None,
    page=1,
    limit=10,
    sort_by="id",
    sort_order="asc"
):

    if page < 1:

        raise HTTPException(
            status_code=400,
            detail="Page must be greater than 0"
        )

    if limit < 1 or limit > 100:

        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 100"
        )

    query = package_repository.search_packages(
        db=db,
        destination=destination,
        min_price=min_price,
        max_price=max_price,
        duration=duration,
        package_date=package_date,
        availability=availability,
        min_rating=min_rating
    )

    # Sorting
    allowed_sort_fields = {
        "id": "id",
        "price": "price",
        "duration": "duration"
    }

    if sort_by not in allowed_sort_fields:

        raise HTTPException(
            status_code=400,
            detail="Invalid sort field"
        )

    if sort_order not in ["asc", "desc"]:

        raise HTTPException(
            status_code=400,
            detail="sort_order must be asc or desc"
        )

    column = getattr(
        package_repository.Package,
        allowed_sort_fields[sort_by]
    )

    if sort_order == "desc":

        query = query.order_by(
            column.desc()
        )

    else:

        query = query.order_by(
            column.asc()
        )

    # Total count
    total = query.count()

    # Pagination
    offset = (page - 1) * limit

    packages = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_pages = (
        (total + limit - 1) // limit
    )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "data": packages
    }


# CACHE PACKAGE DATA ------------------------------------------------------


def get_package_by_id(
    db,
    package_id: int
):

    cache_key = f"package:{package_id}"

    cached_data = redis_client.get(
        cache_key
    )

    if cached_data:

        return json.loads(
            cached_data
        )

    package = (
        package_repository
        .get_package_by_id(
            db,
            package_id
        )
    )

    if not package:

        raise HTTPException(
            status_code=404,
            detail="Package not found"
        )

    data = {
        "id": package.id,
        "package_name":
            package.package_name,
        "price":
            float(package.price)
    }

    redis_client.setex(
        cache_key,
        300,
        json.dumps(data)
    )

    return data

package_service = PackageService()
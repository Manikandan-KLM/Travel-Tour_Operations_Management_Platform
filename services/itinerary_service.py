from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.itinerary_model import Itinerary

from repositories.itinerary_repository import (
    itinerary_repository
)

from repositories.package_repository import (
    package_repository
)

from schemas.itinerary_schema import (
    ItineraryCreate,
    ItineraryUpdate
)


class ItineraryService:

    def create_itinerary(
        self,
        db: Session,
        package_id: int,
        data: ItineraryCreate
    ):

        # --------------------------------
        # 1. Check package
        # --------------------------------

        package = package_repository.get_by_id(
            db,
            package_id
        )

        if not package:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Package not found"
            )

        # --------------------------------
        # 2. Day number validation
        # --------------------------------

        if data.day_number > package.duration_days:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Itinerary day cannot exceed "
                    "package duration"
                )
            )

        # --------------------------------
        # 3. Duplicate day validation
        # --------------------------------

        existing = (
            itinerary_repository
            .get_by_package_and_day(
                db,
                package_id,
                data.day_number
            )
        )

        if existing:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Itinerary day already exists "
                    "for this package"
                )
            )

        # --------------------------------
        # 4. Time validation
        # --------------------------------

        if data.end_time <= data.start_time:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End time must be after start time"
            )

        # --------------------------------
        # 5. Create
        # --------------------------------

        itinerary = Itinerary(
            package_id=package_id,
            day_number=data.day_number,
            title=data.title,
            description=data.description,
            location=data.location,
            start_time=data.start_time,
            end_time=data.end_time
        )

        try:

            return itinerary_repository.create(
                db,
                itinerary
            )

        except IntegrityError:

            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Itinerary day already exists "
                    "for this package"
                )
            )

    # ------------------------------------
    # GET ALL ITINERARY
    # ------------------------------------

    def get_package_itinerary(
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

        return itinerary_repository.get_by_package(
            db,
            package_id
        )

    # ------------------------------------
    # GET ONE
    # ------------------------------------

    def get_itinerary(
        self,
        db: Session,
        itinerary_id: int
    ):

        itinerary = itinerary_repository.get_by_id(
            db,
            itinerary_id
        )

        if not itinerary:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Itinerary not found"
            )

        return itinerary

    # ------------------------------------
    # UPDATE
    # ------------------------------------

    def update_itinerary(
        self,
        db: Session,
        itinerary_id: int,
        data: ItineraryUpdate
    ):

        itinerary = self.get_itinerary(
            db,
            itinerary_id
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        # --------------------------------
        # New day number
        # --------------------------------

        new_day_number = update_data.get(
            "day_number",
            itinerary.day_number
        )

        # --------------------------------
        # Check package duration
        # --------------------------------

        package = package_repository.get_by_id(
            db,
            itinerary.package_id
        )

        if not package:

            raise HTTPException(
                status_code=404,
                detail="Package not found"
            )

        if new_day_number > package.duration_days:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Itinerary day cannot exceed "
                    "package duration"
                )
            )

        # --------------------------------
        # Check duplicate day
        # --------------------------------

        if new_day_number != itinerary.day_number:

            existing = (
                itinerary_repository
                .get_by_package_and_day(
                    db,
                    itinerary.package_id,
                    new_day_number
                )
            )

            if existing:

                raise HTTPException(
                    status_code=409,
                    detail=(
                        "Itinerary day already exists "
                        "for this package"
                    )
                )

        # --------------------------------
        # Time validation
        # --------------------------------

        new_start_time = update_data.get(
            "start_time",
            itinerary.start_time
        )

        new_end_time = update_data.get(
            "end_time",
            itinerary.end_time
        )

        if new_end_time <= new_start_time:

            raise HTTPException(
                status_code=400,
                detail="End time must be after start time"
            )

        # --------------------------------
        # Update fields
        # --------------------------------

        for field, value in update_data.items():

            setattr(
                itinerary,
                field,
                value
            )

        return itinerary_repository.update(
            db,
            itinerary
        )

    # ------------------------------------
    # DELETE
    # ------------------------------------

    def delete_itinerary(
        self,
        db: Session,
        itinerary_id: int
    ):

        itinerary = self.get_itinerary(
            db,
            itinerary_id
        )

        itinerary_repository.delete(
            db,
            itinerary
        )

        return {
            "message": "Itinerary deleted successfully"
        }


itinerary_service = ItineraryService()
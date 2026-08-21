from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.traveler_model import Traveler

from repositories.booking_repository import (
    booking_repository
)

from repositories.traveler_repository import (
    traveler_repository
)

from schemas.traveler_schema import (
    TravelerCreate,
    TravelerUpdate
)


class TravelerService:

    def create_traveler(
        self,
        db: Session,
        booking_id: int,
        data: TravelerCreate
    ):

        # --------------------------------
        # 1. Check booking
        # --------------------------------

        booking = booking_repository.get_by_id(
            db,
            booking_id
        )

        if not booking:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )

        # --------------------------------
        # 2. Date of birth validation
        # --------------------------------

        if data.date_of_birth >= date.today():

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Date of birth must be in the past"
            )

        # --------------------------------
        # 3. Create traveler
        # --------------------------------

        traveler = Traveler(
            booking_id=booking_id,
            full_name=data.full_name,
            date_of_birth=data.date_of_birth,
            gender=data.gender,
            passport_number=data.passport_number,
            nationality=data.nationality,
            special_requirements=data.special_requirements
        )

        return traveler_repository.create(
            db,
            traveler
        )

    # ------------------------------------
    # GET TRAVELERS
    # ------------------------------------

    def get_booking_travelers(
        self,
        db: Session,
        booking_id: int
    ):

        booking = booking_repository.get_by_id(
            db,
            booking_id
        )

        if not booking:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )

        return traveler_repository.get_by_booking(
            db,
            booking_id
        )

    # ------------------------------------
    # UPDATE TRAVELER
    # ------------------------------------

    def update_traveler(
        self,
        db: Session,
        traveler_id: int,
        data: TravelerUpdate
    ):

        traveler = traveler_repository.get_by_id(
            db,
            traveler_id
        )

        if not traveler:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Traveler not found"
            )

        update_data = data.model_dump(
            exclude_unset=True
        )

        # Date validation
        if "date_of_birth" in update_data:

            if update_data["date_of_birth"] >= date.today():

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Date of birth must be in the past"
                )

        for field, value in update_data.items():

            setattr(
                traveler,
                field,
                value
            )

        return traveler_repository.update(
            db,
            traveler
        )


traveler_service = TravelerService()
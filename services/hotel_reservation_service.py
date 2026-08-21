from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.hotel_reservation_model import (
    HotelReservation
)

from repositories.booking_repository import (
    booking_repository
)

from repositories.room_repository import (
    room_repository
)

from repositories.hotel_reservation_repository import (
    hotel_reservation_repository
)

from schemas.hotel_reservation_schema import (
    HotelReservationCreate
)


class HotelReservationService:

    def create_reservation(
        self,
        db: Session,
        data: HotelReservationCreate
    ):

        # ---------------------------------
        # 1. Validate dates
        # ---------------------------------

        if data.check_out <= data.check_in:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Check-out must be after check-in"
                )
            )

        # ---------------------------------
        # 2. Check Booking
        # ---------------------------------

        booking = booking_repository.get_by_id(
            db,
            data.booking_id
        )

        if not booking:

            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        # ---------------------------------
        # 3. Booking status
        # ---------------------------------

        if booking.booking_status != "Confirmed":

            raise HTTPException(
                status_code=400,
                detail=(
                    "Hotel reservation requires "
                    "a confirmed booking"
                )
            )

        # ---------------------------------
        # 4. Check Room
        # ---------------------------------

        room = room_repository.get_by_id(
            db,
            data.room_id
        )

        if not room:

            raise HTTPException(
                status_code=404,
                detail="Room not found"
            )

        # ---------------------------------
        # 5. Room availability
        # ---------------------------------

        if room.availability_status != "Available":

            raise HTTPException(
                status_code=400,
                detail="Room is not available"
            )

        # ---------------------------------
        # 6. Capacity Check
        # ---------------------------------

        total_travelers = (
            booking.number_of_travelers
        )

        total_capacity = (
            room.capacity
            * data.number_of_rooms
        )

        if total_capacity < total_travelers:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Room capacity is not enough "
                    "for the travelers"
                )
            )

        # ---------------------------------
        # 7. Overlap Check
        # ---------------------------------

        overlapping = (
            hotel_reservation_repository
            .find_overlapping(
                db,
                data.room_id,
                data.check_in,
                data.check_out
            )
        )

        if overlapping:

            raise HTTPException(
                status_code=409,
                detail=(
                    "Room is already reserved "
                    "for the selected dates"
                )
            )

        # ---------------------------------
        # 8. Calculate nights
        # ---------------------------------

        number_of_nights = (
            data.check_out
            - data.check_in
        ).days

        # ---------------------------------
        # 9. Calculate hotel cost
        # ---------------------------------

        total_amount = (
            room.price_per_night
            * data.number_of_rooms
            * number_of_nights
        )

        # ---------------------------------
        # 10. Create reservation
        # ---------------------------------

        reservation = HotelReservation(
            booking_id=data.booking_id,
            room_id=data.room_id,
            check_in=data.check_in,
            check_out=data.check_out,
            number_of_rooms=data.number_of_rooms,
            total_amount=total_amount
        )

        return hotel_reservation_repository.create(
            db,
            reservation
        )

    def get_reservations(
        self,
        db: Session
    ):

        return hotel_reservation_repository.get_all(
            db
        )


hotel_reservation_service = (
    HotelReservationService()
)
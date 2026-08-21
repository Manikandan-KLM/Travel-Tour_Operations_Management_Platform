from sqlalchemy.orm import Session

from models.hotel_reservation_model import (
    HotelReservation
)


class HotelReservationRepository:

    def create(
        self,
        db: Session,
        reservation: HotelReservation
    ):

        db.add(reservation)
        db.commit()
        db.refresh(reservation)

        return reservation

    def get_all(
        self,
        db: Session
    ):

        return (
            db.query(
                HotelReservation
            )
            .order_by(
                HotelReservation.id.desc()
            )
            .all()
        )

    def find_overlapping(
        self,
        db: Session,
        room_id: int,
        check_in,
        check_out
    ):

        return (
            db.query(
                HotelReservation
            )
            .filter(
                HotelReservation.room_id == room_id,

                HotelReservation.check_in < check_out,

                HotelReservation.check_out > check_in
            )
            .first()
        )


hotel_reservation_repository = (
    HotelReservationRepository()
)
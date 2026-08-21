from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from models.booking_model import Booking
from models.payment_model import Payment


class BookingRepository:

    def create(
        self,
        db: Session,
        booking: Booking
    ):

        db.add(booking)

        db.commit()

        db.refresh(booking)

        return booking

    def get_by_id(
        self,
        db: Session,
        booking_id: int
    ):

        return (
            db.query(Booking)
            .filter(
                Booking.id == booking_id
            )
            .first()
        )

    def get_all(
        self,
        db: Session
    ):

        return (
            db.query(Booking)
            .order_by(
                Booking.id.desc()
            )
            .all()
        )

    def find_active_booking(
        self,
        db: Session,
        customer_id: int,
        package_id: int
    ):

        return (
            db.query(Booking)
            .filter(
                Booking.customer_id == customer_id,
                Booking.package_id == package_id,
                Booking.booking_status.in_(
                    ["Pending", "Confirmed"]
                )
            )
            .first()
        )

    def update(
        self,
        db: Session,
        booking: Booking
    ):

        db.commit()

        db.refresh(booking)

        return booking


def search_bookings(
    db: Session,
    booking_status=None,
    payment_status=None,
    booking_date=None
):

    query = (
        db.query(Booking)
        .outerjoin(
            Payment,
            Payment.booking_id == Booking.id
        )
    )

    # Booking status
    if booking_status:

        query = query.filter(
            Booking.status == booking_status
        )

    # Payment status
    if payment_status:

        query = query.filter(
            Payment.payment_status == payment_status
        )

    # Booking date
    if booking_date:

        start = datetime.combine(
        booking_date,
        datetime.min.time()
    )

    end = start + timedelta(days=1)

    query = query.filter(
        Booking.created_at >= start,
        Booking.created_at < end
    )

    return query


booking_repository = BookingRepository()
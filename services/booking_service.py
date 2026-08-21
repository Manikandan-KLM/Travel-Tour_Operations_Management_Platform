from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.booking_model import Booking

from repositories.booking_repository import (
    booking_repository
)

from repositories.customer_repository import (
    customer_repository
)

from repositories.package_repository import (
    package_repository
)

from services import notification_service

from schemas.booking_schema import BookingCreate

from fastapi import BackgroundTasks

class BookingService:

    # ==========================================
    # CREATE BOOKING
    # ==========================================

    def create_booking(
        self,
        db: Session,
        data: BookingCreate
    ):

        # --------------------------------------
        # 1. Check Customer
        # --------------------------------------

        customer = customer_repository.get_by_id(
            db,
            data.customer_id
        )

        if not customer:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        # --------------------------------------
        # 2. Check Package
        # --------------------------------------

        package = package_repository.get_by_id(
            db,
            data.package_id
        )

        if not package:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Package not found"
            )

        # --------------------------------------
        # 3. Cancelled Package Check
        # --------------------------------------

        if package.status == "Cancelled":

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cancelled package cannot be booked"
            )

        # --------------------------------------
        # 4. Completed Package Check
        # --------------------------------------

        if package.status == "Completed":

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Completed package cannot be booked"
            )

        # --------------------------------------
        # 5. Duplicate Booking Check
        # --------------------------------------

        existing = (
            booking_repository.find_active_booking(
                db,
                data.customer_id,
                data.package_id
            )
        )

        if existing:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Customer already has an active "
                    "booking for this package"
                )
            )

        # --------------------------------------
        # 6. Capacity Check
        # --------------------------------------

        if (
            data.number_of_travelers
            > package.available_slots
        ):

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Not enough available slots "
                    "for this package"
                )
            )

        # --------------------------------------
        # 7. Calculate Base Amount
        # --------------------------------------

        base_amount = (
            package.base_price
            * data.number_of_travelers
        )

        # --------------------------------------
        # 8. Validate Discount
        # --------------------------------------

        if data.discount > base_amount:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Discount cannot be greater "
                    "than base amount"
                )
            )

        # --------------------------------------
        # 9. Calculate Total
        # --------------------------------------

        total_amount = (
            base_amount
            + data.tax
            - data.discount
        )

        # --------------------------------------
        # 10. Create Booking
        # --------------------------------------

        booking = Booking(
            customer_id=data.customer_id,
            package_id=data.package_id,
            booking_date=date.today(),
            number_of_travelers=data.number_of_travelers,
            base_amount=base_amount,
            discount=data.discount,
            tax=data.tax,
            total_amount=total_amount,
            booking_status="Confirmed"
        )

        # --------------------------------------
        # 11. Reduce Available Slots
        # --------------------------------------

        package.available_slots -= (
            data.number_of_travelers
        )

        # --------------------------------------
        # 12. Package Full
        # --------------------------------------

        if package.available_slots == 0:

            package.status = "Full"

        booking_repository.create(
            db,
            booking
        )

        return booking

    # ==========================================
    # GET ALL BOOKINGS
    # ==========================================

    def get_bookings(
        self,
        db: Session
    ):

        return booking_repository.get_all(db)

    # ==========================================
    # GET BOOKING
    # ==========================================

    def get_booking(
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

        return booking

    # ==========================================
    # CANCEL BOOKING
    # ==========================================

    def cancel_booking(
        self,
        db: Session,
        booking_id: int
    ):

        booking = self.get_booking(
            db,
            booking_id
        )

        # --------------------------------------
        # Already Cancelled
        # --------------------------------------

        if booking.booking_status == "Cancelled":

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Booking is already cancelled"
            )

        # --------------------------------------
        # Completed Booking
        # --------------------------------------

        if booking.booking_status == "Completed":

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Completed booking cannot be cancelled"
                )
            )

        # --------------------------------------
        # Restore slots only when needed
        # --------------------------------------

        if booking.booking_status == "Confirmed":

            package = package_repository.get_by_id(
                db,
                booking.package_id
            )

            if package:

                package.available_slots += (
                    booking.number_of_travelers
                )

                # If package was Full,
                # it can become Published again
                if package.status == "Full":

                    package.status = "Published"

        # --------------------------------------
        # Cancel Booking
        # --------------------------------------

        booking.booking_status = "Cancelled"

        return booking_repository.update(
            db,
            booking
        )



def search_bookings(
    db: Session,
    booking_status=None,
    payment_status=None,
    booking_date=None,
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

    query = booking_repository.search_bookings(
        db=db,
        booking_status=booking_status,
        payment_status=payment_status,
        booking_date=booking_date
    )

    allowed_sort_fields = {
        "id": "id",
        "created_at": "created_at",
        "total_amount": "total_amount"
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
        Booking,
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

    total = query.count()

    offset = (page - 1) * limit

    bookings = (
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
        "data": bookings
    }

def confirm_booking(
    db,
    booking_id,
    background_tasks
):

    booking = booking_repository.get_booking_by_id(
        db,
        booking_id
    )

    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    booking.status = "Confirmed"

    db.commit()

    background_tasks.add_task(
        notification_service.send_booking_confirmation,

        db,

        booking.customer_id,

        booking.customer.email,

        booking.id,

        booking.package.name
    )

    return booking


booking_service = BookingService()
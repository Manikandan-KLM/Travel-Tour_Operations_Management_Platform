from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.cancellation_model import Cancellation

from repositories import (
    booking_repository,
    payment_repository,
    cancellation_repository
)


def calculate_refund_percentage(
    days_remaining: int
):

    if days_remaining >= 15:

        return 90.0

    elif days_remaining >= 7:

        return 70.0

    elif days_remaining >= 2:

        return 40.0

    else:

        return 0.0


def calculate_refund_amount(
    paid_amount: float,
    refund_percentage: float
):

    return round(
        paid_amount * refund_percentage / 100,
        2
    )


def cancel_booking(
    db: Session,
    booking_id: int,
    cancellation_data
):

    # --------------------------------
    # 1. Find Booking
    # --------------------------------

    booking = booking_repository.get_booking_by_id(
        db,
        booking_id
    )

    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    # --------------------------------
    # 2. Check Already Cancelled
    # --------------------------------

    if booking.status == "Cancelled":

        raise HTTPException(
            status_code=400,
            detail="Booking is already cancelled"
        )

    # --------------------------------
    # 3. Find Existing Cancellation
    # --------------------------------

    existing_cancellation = (
        cancellation_repository
        .get_cancellation_by_booking_id(
            db,
            booking_id
        )
    )

    if existing_cancellation:

        raise HTTPException(
            status_code=400,
            detail="Cancellation already exists"
        )

    # --------------------------------
    # 4. Get Tour Date
    # --------------------------------

    tour_date = booking.tour_date

    current_date = datetime.utcnow()

    # --------------------------------
    # 5. Calculate Days Remaining
    # --------------------------------

    days_remaining = (
        tour_date.date()
        - current_date.date()
    ).days

    # --------------------------------
    # 6. Get Refund Percentage
    # --------------------------------

    refund_percentage = calculate_refund_percentage(
        days_remaining
    )

    # --------------------------------
    # 7. Get Successful Payments
    # --------------------------------

    payments = (
        payment_repository
        .get_successful_payments_by_booking(
            db,
            booking_id
        )
    )

    paid_amount = sum(
        payment.amount
        for payment in payments
    )

    # --------------------------------
    # 8. Calculate Refund
    # --------------------------------

    refund_amount = calculate_refund_amount(
        paid_amount,
        refund_percentage
    )

    # --------------------------------
    # 9. Create Cancellation
    # --------------------------------

    cancellation = Cancellation(

        booking_id=booking_id,

        cancellation_reason=(
            cancellation_data.cancellation_reason
        ),

        cancellation_date=current_date,

        refund_percentage=refund_percentage,

        refund_amount=refund_amount
    )

    cancellation = (
        cancellation_repository
        .create_cancellation(
            db,
            cancellation
        )
    )

    # --------------------------------
    # 10. Update Booking
    # --------------------------------

    booking.status = "Cancelled"

    booking_repository.update_booking(
        db,
        booking
    )

    # --------------------------------
    # 11. Refund Payment
    # --------------------------------

    if refund_amount > 0:

        remaining_refund = refund_amount

        for payment in payments:

            if remaining_refund <= 0:
                break

            payment_refund = min(
                payment.amount,
                remaining_refund
            )

            # Current simple implementation:
            # mark payment as refunded
            if payment_refund == payment.amount:

                payment.payment_status = "Refunded"

            remaining_refund -= payment_refund

            payment_repository.update_payment(
                db,
                payment
            )

    return cancellation
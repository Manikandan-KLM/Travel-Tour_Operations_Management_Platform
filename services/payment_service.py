from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.payment_model import Payment

from repositories import (
    payment_repository,
    booking_repository
)

from services import notification_service


ALLOWED_PAYMENT_METHODS = [
    "UPI",
    "Card",
    "Net Banking",
    "Wallet"
]


def create_payment(
    db: Session,
    booking_id: int,
    payment_data
):

    # --------------------------------
    # 1. Check Booking
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
    # 2. Validate Payment Method
    # --------------------------------

    if payment_data.payment_method not in ALLOWED_PAYMENT_METHODS:

        raise HTTPException(
            status_code=400,
            detail="Invalid payment method"
        )

    # --------------------------------
    # 3. Check Duplicate Transaction
    # --------------------------------

    existing_transaction = (
        payment_repository
        .get_payment_by_transaction_id(
            db,
            payment_data.transaction_id
        )
    )

    if existing_transaction:

        raise HTTPException(
            status_code=400,
            detail="Duplicate transaction ID"
        )

    # --------------------------------
    # 4. Check Payment Amount
    # --------------------------------

    if payment_data.amount > booking.total_amount:

        raise HTTPException(
            status_code=400,
            detail="Payment cannot exceed booking amount"
        )

    # --------------------------------
    # 5. Create Payment
    # --------------------------------

    payment = Payment(

        booking_id=booking_id,

        amount=payment_data.amount,

        payment_method=payment_data.payment_method,

        transaction_id=payment_data.transaction_id,

        payment_status="Success",

        payment_date=datetime.utcnow()
    )

    payment = payment_repository.create_payment(
        db,
        payment
    )

    # --------------------------------
    # 6. Confirm Booking
    # --------------------------------

    if payment.payment_status == "Success":

        booking.status = "Confirmed"

        booking_repository.update_booking(
            db,
            booking
        )

    return payment


def get_all_payments(
    db: Session
):

    return payment_repository.get_all_payments(
        db
    )


def get_payment(
    db: Session,
    payment_id: int
):

    payment = payment_repository.get_payment_by_id(
        db,
        payment_id
    )

    if not payment:

        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment


def refund_payment(
    db: Session,
    payment_id: int
):

    payment = payment_repository.get_payment_by_id(
        db,
        payment_id
    )

    if not payment:

        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    # --------------------------------
    # Check Payment Status
    # --------------------------------

    if payment.payment_status != "Success":

        raise HTTPException(
            status_code=400,
            detail="Only successful payments can be refunded"
        )

    # --------------------------------
    # Refund Amount
    # --------------------------------

    refund_amount = payment.amount

    if refund_amount > payment.amount:

        raise HTTPException(
            status_code=400,
            detail="Refund cannot exceed paid amount"
        )

    # --------------------------------
    # Update Payment
    # --------------------------------

    payment.payment_status = "Refunded"

    return payment_repository.update_payment(
        db,
        payment
    )


def mark_payment_success(
    db,
    payment,
    background_tasks
):

    payment.payment_status = "Success"

    db.commit()

    background_tasks.add_task(
        notification_service.send_payment_success,

        db,

        payment.booking.customer_id,

        payment.booking.customer.email,

        payment.id,

        payment.amount
    )

    return payment


def mark_payment_failed(
    db,
    payment,
    background_tasks
):

    payment.payment_status = "Failed"

    db.commit()

    background_tasks.add_task(
        notification_service.send_payment_failure,

        db,

        payment.booking.customer_id,

        payment.booking.customer.email,

        payment.id
    )

    return payment
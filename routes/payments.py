from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database import get_db

from schemas.payment_schema import (
    PaymentCreate,
    PaymentResponse
)

from services import payment_service


router = APIRouter(prefix="/payments",tags=["Payments"])


# --------------------------------
# CREATE PAYMENT
# --------------------------------

@router.post(
    "/{booking_id}",
    response_model=PaymentResponse
)
def create_payment(
    booking_id: int,
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):

    return payment_service.create_payment(
        db=db,
        booking_id=booking_id,
        payment_data=payment
    )


# --------------------------------
# GET ALL PAYMENTS
# --------------------------------

@router.get(
    "/",
    response_model=list[PaymentResponse]
)
def get_payments(
    db: Session = Depends(get_db)
):

    return payment_service.get_all_payments(
        db
    )


# --------------------------------
# GET PAYMENT
# --------------------------------

@router.get(
    "/{payment_id}",
    response_model=PaymentResponse
)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):

    return payment_service.get_payment(
        db=db,
        payment_id=payment_id
    )


# --------------------------------
# REFUND
# --------------------------------

@router.post(
    "/{payment_id}/refund",
    response_model=PaymentResponse
)
def refund_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):

    return payment_service.refund_payment(
        db=db,
        payment_id=payment_id
    )
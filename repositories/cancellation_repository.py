from sqlalchemy.orm import Session

from models import Cancellation, Payment


def create_cancellation(
    db: Session,
    cancellation: Cancellation
):

    db.add(cancellation)

    db.commit()

    db.refresh(cancellation)

    return cancellation


def get_cancellation_by_booking_id(
    db: Session,
    booking_id: int
):

    return db.query(Cancellation).filter(
        Cancellation.booking_id == booking_id
    ).first()


def get_all_cancellations(
    db: Session
):

    return db.query(Cancellation).all()


def update_payment(
    db: Session,
    payment: Payment
):

    db.commit()

    db.refresh(payment)

    return payment
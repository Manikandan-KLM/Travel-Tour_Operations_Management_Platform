from sqlalchemy.orm import Session

from models.payment_model import Payment


def create_payment(
    db: Session,
    payment: Payment
):

    db.add(payment)

    db.commit()

    db.refresh(payment)

    return payment


def get_all_payments(
    db: Session
):

    return db.query(Payment).all()


def get_payment_by_id(
    db: Session,
    payment_id: int
):

    return db.query(Payment).filter(
        Payment.id == payment_id
    ).first()


def get_payment_by_transaction_id(
    db: Session,
    transaction_id: str
):

    return db.query(Payment).filter(
        Payment.transaction_id == transaction_id
    ).first()


def get_payment_by_booking_id(
    db: Session,
    booking_id: int
):

    return db.query(Payment).filter(
        Payment.booking_id == booking_id
    ).first()


def update_payment(
    db: Session,
    payment: Payment
):

    db.commit()

    db.refresh(payment)

    return payment
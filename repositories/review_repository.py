from sqlalchemy.orm import Session

from models.review_model import Review


def create_review(
    db: Session,
    review: Review
):

    db.add(review)

    db.commit()

    db.refresh(review)

    return review


def get_review_by_id(
    db: Session,
    review_id: int
):

    return db.query(Review).filter(
        Review.id == review_id
    ).first()


def get_review_by_booking_id(
    db: Session,
    booking_id: int
):

    return db.query(Review).filter(
        Review.booking_id == booking_id
    ).first()


def get_reviews_by_package_id(
    db: Session,
    package_id: int
):

    return db.query(Review).filter(
        Review.package_id == package_id
    ).all()


def update_review(
    db: Session,
    review: Review
):

    db.commit()

    db.refresh(review)

    return review


def delete_review(
    db: Session,
    review: Review
):

    db.delete(review)

    db.commit()
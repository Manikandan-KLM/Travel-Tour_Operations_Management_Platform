from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.review_model import Review

from repositories import (
    review_repository,
    booking_repository,
    customer_repository
)

def create_review(
    db: Session,
    review_data
):

    # --------------------------------
    # 1. Check Customer
    # --------------------------------

    customer = (
        customer_repository
        .get_customer_by_id(
            db,
            review_data.customer_id
        )
    )

    if not customer:

        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # --------------------------------
    # 2. Check Booking
    # --------------------------------

    booking = (
        booking_repository
        .get_booking_by_id(
            db,
            review_data.booking_id
        )
    )

    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    # --------------------------------
    # 3. Check Customer owns booking
    # --------------------------------

    if booking.customer_id != review_data.customer_id:

        raise HTTPException(
            status_code=403,
            detail="Customer does not own this booking"
        )

    # --------------------------------
    # 4. Check Package
    # --------------------------------

    if booking.package_id != review_data.package_id:

        raise HTTPException(
            status_code=400,
            detail="Booking does not belong to this package"
        )

    # --------------------------------
    # 5. Check Booking Completed
    # --------------------------------

    if booking.status != "Completed":

        raise HTTPException(
            status_code=400,
            detail="Only customers with completed bookings can review"
        )

    # --------------------------------
    # 6. Check Existing Review
    # --------------------------------

    existing_review = (
        review_repository
        .get_review_by_booking_id(
            db,
            review_data.booking_id
        )
    )

    if existing_review:

        raise HTTPException(
            status_code=400,
            detail="A review already exists for this booking"
        )

    # --------------------------------
    # 7. Create Review
    # --------------------------------

    review = Review(

        customer_id=review_data.customer_id,

        package_id=review_data.package_id,

        booking_id=review_data.booking_id,

        rating=review_data.rating,

        review_text=review_data.review_text
    )

    return review_repository.create_review(
        db,
        review
    )


def get_package_reviews(
    db: Session,
    package_id: int
):

    return (
        review_repository
        .get_reviews_by_package_id(
            db,
            package_id
        )
    )

def get_review(
    db: Session,
    review_id: int
):

    review = (
        review_repository
        .get_review_by_id(
            db,
            review_id
        )
    )

    if not review:

        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    return review


def update_review(
    db: Session,
    review_id: int,
    customer_id: int,
    review_data
):

    # --------------------------------
    # Find Review
    # --------------------------------

    review = (
        review_repository
        .get_review_by_id(
            db,
            review_id
        )
    )

    if not review:

        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    # --------------------------------
    # Check Owner
    # --------------------------------

    if review.customer_id != customer_id:

        raise HTTPException(
            status_code=403,
            detail="You can update only your own review"
        )

    # --------------------------------
    # Update
    # --------------------------------

    review.rating = review_data.rating

    review.review_text = review_data.review_text

    return review_repository.update_review(
        db,
        review
    )

def delete_review(
    db: Session,
    review_id: int,
    customer_id: int
):

    review = (
        review_repository
        .get_review_by_id(
            db,
            review_id
        )
    )

    if not review:

        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    # --------------------------------
    # Check Owner
    # --------------------------------

    if review.customer_id != customer_id:

        raise HTTPException(
            status_code=403,
            detail="You can delete only your own review"
        )

    review_repository.delete_review(
        db,
        review
    )

    return {
        "message": "Review deleted successfully"
    }
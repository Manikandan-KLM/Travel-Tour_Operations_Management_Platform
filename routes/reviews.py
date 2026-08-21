from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database import get_db

from schemas.review_schema import (
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse
)

from services import review_service


router = APIRouter(prefix="/reviews",tags=["Reviews"])


# --------------------------------
# CREATE REVIEW
# --------------------------------

@router.post(
    "/reviews",
    response_model=ReviewResponse
)
def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db)
):

    return review_service.create_review(
        db,
        review
    )


# --------------------------------
# GET PACKAGE REVIEWS
# --------------------------------

@router.get(
    "/packages/{package_id}/reviews",
    response_model=list[ReviewResponse]
)
def get_package_reviews(
    package_id: int,
    db: Session = Depends(get_db)
):

    return review_service.get_package_reviews(
        db,
        package_id
    )


# --------------------------------
# UPDATE REVIEW
# --------------------------------

@router.put(
    "/reviews/{review_id}",
    response_model=ReviewResponse
)
def update_review(
    review_id: int,
    customer_id: int,
    review: ReviewUpdate,
    db: Session = Depends(get_db)
):

    return review_service.update_review(
        db=db,
        review_id=review_id,
        customer_id=customer_id,
        review_data=review
    )


# --------------------------------
# DELETE REVIEW
# --------------------------------

@router.delete(
    "/reviews/{review_id}"
)
def delete_review(
    review_id: int,
    customer_id: int,
    db: Session = Depends(get_db)
):

    return review_service.delete_review(
        db=db,
        review_id=review_id,
        customer_id=customer_id
    )


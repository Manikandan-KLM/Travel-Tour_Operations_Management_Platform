from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.guide_model import Guide
from repositories.guide_repository import guide_repository

class GuideService:
 def create_guide(
    db: Session,
    guide_data
):

    # -------------------------
    # Check Duplicate Email
    # -------------------------

    existing_guide = (
        guide_repository
        .get_guide_by_email(
            db,
            guide_data.email
        )
    )

    if existing_guide:

        raise HTTPException(
            status_code=400,
            detail="Guide email already exists"
        )

    # -------------------------
    # Validate Status
    # -------------------------

    if guide_data.availability_status not in [
        "Active",
        "Inactive"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Invalid availability status"
        )

    # -------------------------
    # Create Guide
    # -------------------------

    guide = Guide(
        name=guide_data.name,
        email=guide_data.email,
        phone=guide_data.phone,
        specialization=guide_data.specialization,
        availability_status=guide_data.availability_status
    )

    return guide_repository.create_guide(
        db,
        guide
    )


def get_all_guides(
    db: Session
):

    return guide_repository.get_all_guides(db)
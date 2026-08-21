from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.activity_model import Activity
from repositories.activity_repository import activity_repository
from repositories.guide_repository import guide_repository
from models.package_model import TourPackage

class ActivityService:

 def create_activity(
    db: Session,
    activity_data
):

    # -------------------------
    # Validate Package
    # -------------------------

    package = db.query(TourPackage).filter(
        TourPackage.id == activity_data.package_id
    ).first()

    if not package:

        raise HTTPException(
            status_code=404,
            detail="Package not found"
        )

    # -------------------------
    # Validate Time
    # -------------------------

    if activity_data.end_time <= activity_data.start_time:

        raise HTTPException(
            status_code=400,
            detail="End time must be after start time"
        )

    # -------------------------
    # Create Model
    # -------------------------

    activity = Activity(
        package_id=activity_data.package_id,
        activity_name=activity_data.activity_name,
        location=activity_data.location,
        duration=activity_data.duration,
        price=activity_data.price,
        capacity=activity_data.capacity,
        start_time=activity_data.start_time,
        end_time=activity_data.end_time
    )

    return activity_repository.create_activity(
        db,
        activity
    )


def get_all_activities(
    db: Session
):

    return activity_repository.get_all_activities(db)


def assign_guide(
    db: Session,
    package_id: int,
    guide_id: int
):

    # -------------------------
    # Find Activity
    # -------------------------

    activity = (
        activity_repository
        .get_activity_by_package(
            db,
            package_id
        )
    )

    if not activity:

        raise HTTPException(
            status_code=404,
            detail="Activity not found"
        )

    # -------------------------
    # Find Guide
    # -------------------------

    guide = guide_repository.get_guide_by_id(
        db,
        guide_id
    )

    if not guide:

        raise HTTPException(
            status_code=404,
            detail="Guide not found"
        )

    # -------------------------
    # Check Guide Status
    # -------------------------

    if guide.availability_status != "Active":

        raise HTTPException(
            status_code=400,
            detail="Inactive guide cannot be assigned"
        )

    # -------------------------
    # Check Overlapping Tours
    # -------------------------

    overlapping_activity = (
        activity_repository
        .get_overlapping_activity(
            db=db,
            guide_id=guide_id,
            start_time=activity.start_time,
            end_time=activity.end_time,
            activity_id=activity.id
        )
    )

    if overlapping_activity:

        raise HTTPException(
            status_code=400,
            detail="Guide already assigned to an overlapping tour"
        )

    # -------------------------
    # Assign Guide
    # -------------------------

    activity.guide_id = guide_id

    return activity_repository.update_activity(
        db,
        activity
    )
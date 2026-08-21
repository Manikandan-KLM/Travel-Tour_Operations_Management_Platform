from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from schemas.activity_schema import (
    ActivityCreate,
    ActivityResponse
)

from services.activity_service import ActivityService


router = APIRouter(prefix="/activities",tags=["Activities"])


@router.post(
    "/",
    response_model=ActivityResponse
)
def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db)
):

    return  ActivityService.create_activity(
        db,
        activity
    )


@router.get(
    "/",
    response_model=list[ActivityResponse]
)
def get_activities(
    db: Session = Depends(get_db)
):

    return  ActivityService.get_all_activities(
        db
    )


@router.post(
    "/packages/{package_id}/assign-guide/{guide_id}",
    response_model=ActivityResponse
)
def assign_guide(
    package_id: int,
    guide_id: int,
    db: Session = Depends(get_db)
):

    return  ActivityService.assign_guide(
        db=db,
        package_id=package_id,
        guide_id=guide_id
    )
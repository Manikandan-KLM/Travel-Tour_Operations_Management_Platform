from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from schemas.guide_schema import (
    GuideCreate,
    GuideResponse
)

from services.guide_service import GuideService


router = APIRouter(prefix="/guides",tags=["Guides"])


@router.post(
    "/",
    response_model=GuideResponse
)
def create_guide(
    guide: GuideCreate,
    db: Session = Depends(get_db)
):

    return GuideService.create_guide(
        db,
        guide
    )


@router.get(
    "/",
    response_model=list[GuideResponse]
)
def get_guides(
    db: Session = Depends(get_db)
):

    return GuideService.get_all_guides(
        db
    )
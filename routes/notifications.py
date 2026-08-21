from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from database import get_db

from repositories import notification_repository


router = APIRouter(prefix="/notifications",tags=["Notifications"])


@router.get("/{customer_id}")
def get_notifications(
    customer_id: int,
    db: Session = Depends(get_db)
):

    return notification_repository.get_customer_notifications(
        db,
        customer_id
    )
from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from database import get_db

from services import dashboard_service

from auth.dependencies import (
    require_admin
)


router = APIRouter(prefix="/admin/dashboard",tags=["Admin Dashboard"])


@router.get("/")
def get_dashboard(

    db: Session = Depends(get_db),

    current_user = Depends(
        require_admin
    )
):

    return dashboard_service.get_dashboard(
        db
    )
from fastapi import APIRouter, Depends, status, BackgroundTasks, WebSocket
from sqlalchemy.orm import Session
from datetime import date


from auth.dependencies import (
    get_current_user,
    require_roles
)

from database import get_db

from schemas.booking_schema import (
    BookingCreate,
    BookingResponse
)

from utils.qr_code import generate_booking_qr

from services.booking_service import (
    booking_service
)

from websocket.booking_ws import manager


router = APIRouter(prefix="/bookings",tags=["Bookings"])

# POST BOOKINGS ------------------------------------------------------------------------

@router.post(
    "",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED
)
def create_booking(
    data: BookingCreate,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            "Super Admin",
            "Tour Manager",
            "Booking Agent"
        )
    )
):

    return booking_service.create_booking(
        db,
        data
    )

# GET BOOKINGS -----------------------------------------------------------------------

@router.get(
    "",
    response_model=list[BookingResponse]
)
def get_bookings(
    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            "Super Admin",
            "Tour Manager",
            "Booking Agent"
        )
    )
):

    return booking_service.get_bookings(db)

# GET BOOKINGS BY ID ------------------------------------------------------------------------

@router.get(
    "/{booking_id}",
    response_model=BookingResponse
)
def get_booking(
    booking_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(
        get_current_user
    )
):

    return booking_service.get_booking(
        db,
        booking_id
    )

# CANCEL API ------------------------------------------------------------------------

@router.put(
    "/{booking_id}/cancel",
    response_model=BookingResponse
)
def cancel_booking(
    booking_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            "Super Admin",
            "Tour Manager",
            "Booking Agent"
        )
    )
):

    return booking_service.cancel_booking(
        db,
        booking_id
    )

def search_bookings(

    booking_status: str | None = None,

    payment_status: str | None = None,

    booking_date: date | None = None,

    page: int = 1,

    limit: int = 10,

    sort_by: str = "id",

    sort_order: str = "asc",

    db: Session = Depends(get_db)
):

    return booking_service.search_bookings(

        db=db,

        booking_status=booking_status,

        payment_status=payment_status,

        booking_date=booking_date,

        page=page,

        limit=limit,

        sort_by=sort_by,

        sort_order=sort_order
    )

@router.post("/{booking_id}/confirm")
def confirm_booking(
    booking_id: int,

    background_tasks: BackgroundTasks,

    db: Session = Depends(get_db)
):

    return booking_service.confirm_booking(
        db=db,
        booking_id=booking_id,
        background_tasks=background_tasks
    )

from fastapi.responses import StreamingResponse


@router.get(
    "/{booking_id}/qr"
)
def get_booking_qr(
    booking_id: int
):

    qr_image = generate_booking_qr(
        booking_id
    )

    return StreamingResponse(
        qr_image,
        media_type="image/png"
    )

# WEBSOCKET LIVE BOOKING STATUS ---------------------------------------------


@router.websocket(
    "/ws/bookings"
)
async def booking_websocket(
    websocket: WebSocket
):

    await manager.connect(
        websocket
    )

    try:

        while True:

            await websocket.receive_text()

    except:

        manager.disconnect(
            websocket
        )
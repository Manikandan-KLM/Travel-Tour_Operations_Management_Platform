from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from database import get_db

from services import report_service

from services.pdf_service import generate_booking_pdf

from services import booking_service

from services.excel_service import generate_booking_report



from auth.dependencies import (
    require_admin
)

from repositories import booking_repository

from fastapi.responses import StreamingResponse


router = APIRouter(prefix="/admin/reports",tags=["Admin Reports"])

# DAILY BOOKING ----------------------------------------------------

@router.get(
    "/daily-bookings"
)
def daily_bookings(

    db: Session = Depends(get_db),

    current_user = Depends(
        require_admin
    )
):

    return (
        report_service
        .get_daily_booking_report(
            db
        )
    )

# MONTHLY REVENUE  --------------------------------------------------

@router.get(
    "/monthly-revenue"
)
def monthly_revenue(

    db: Session = Depends(get_db),

    current_user = Depends(
        require_admin
    )
):

    return (
        report_service
        .get_monthly_revenue_report(
            db
        )
    )

# DESTINATION REVENUE -------------------------------------------------------

@router.get(
    "/destination-revenue"
)
def destination_revenue(

    db: Session = Depends(get_db),

    current_user = Depends(
        require_admin
    )
):

    return (
        report_service
        .get_destination_revenue(
            db
        )
    )

# PACKAGE PERFORMANCE ----------------------------------------------------

@router.get(
    "/package-performance"
)
def package_performance(

    db: Session = Depends(get_db),

    current_user = Depends(
        require_admin
    )
):

    return (
        report_service
        .get_package_performance(
            db
        )
    )

# CANCELLATION REPORT --------------------------------------------------------

@router.get(
    "/cancellations"
)
def cancellation_report(

    db: Session = Depends(get_db),

    current_user = Depends(
        require_admin
    )
):

    return (
        report_service
        .get_cancellation_report(
            db
        )
    )

# CUSTOMER BOOKING HISTORY ------------------------------------------------

@router.get(
    "/customers/{customer_id}/booking-history"
)
def customer_booking_history(

    customer_id: int,

    db: Session = Depends(get_db),

    current_user = Depends(
        require_admin
    )
):

    return (
        report_service
        .get_customer_booking_history(
            db,
            customer_id
        )
    )





@router.get(
    "/{booking_id}/confirmation"
)
def download_confirmation(
    booking_id: int,
    db: Session = Depends(get_db)
):

    booking = booking_service.get_booking(
        db,
        booking_id
    )

    pdf = generate_booking_pdf(
        booking
    )

    return StreamingResponse(

        pdf,

        media_type="application/pdf",

        headers={
            "Content-Disposition":
                f"attachment; filename=booking_{booking_id}.pdf"
        }
    )

# EXCEL REPORT EXPORT --------------------------------------------

@router.get(
    "/reports/bookings/export"
)
def export_booking_report(
    db: Session = Depends(get_db)
):

    bookings = (
        booking_repository
        .get_all_bookings(db)
    )

    excel_file = generate_booking_report(
        bookings
    )

    return StreamingResponse(

        excel_file,

        media_type=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

        headers={
            "Content-Disposition":
            "attachment; filename=bookings.xlsx"
        }
    )
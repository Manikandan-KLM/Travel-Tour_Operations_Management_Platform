from fastapi import HTTPException

from repositories import (
    report_repository
)


def get_daily_booking_report(
    db
):

    return (
        report_repository
        .daily_booking_report(db)
    )


def get_monthly_revenue_report(
    db
):

    return (
        report_repository
        .monthly_revenue_report(db)
    )


def get_destination_revenue(
    db
):

    return (
        report_repository
        .destination_wise_revenue(db)
    )


def get_package_performance(
    db
):

    return (
        report_repository
        .package_performance(db)
    )


def get_cancellation_report(
    db
):

    return (
        report_repository
        .cancellation_report(db)
    )


def get_customer_booking_history(
    db,
    customer_id
):

    bookings = (
        report_repository
        .get_customer_booking_history(
            db,
            customer_id
        )
    )

    if not bookings:

        raise HTTPException(
            status_code=404,
            detail="No booking history found"
        )

    return bookings
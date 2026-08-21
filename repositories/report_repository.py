from sqlalchemy import func

from models.booking_model import Booking
from models.payment_model import Payment
from models.destination_model import Destination
from models.package_model import TourPackage
from models.review_model import Review


# DAILY BOOKING REPORT ---------------------------------------------------

def daily_booking_report(
    db
):

    results = (
        db.query(

            func.date(
                Booking.booking_date
            ).label("date"),

            func.count(
                Booking.id
            ).label("total_bookings")

        )
        .group_by(
            func.date(
                Booking.booking_date
            )
        )
        .order_by(
            func.date(
                Booking.booking_date
            )
        )
        .all()
    )

    return [
        {
            "date": str(row.date),

            "total_bookings":
                row.total_bookings
        }

        for row in results
    ]

# MONTHLY REVENUE REPORT -----------------------------------------------

def monthly_revenue_report(
    db
):

    results = (
        db.query(

            func.date_trunc(
                "month",
                Payment.payment_date
            ).label("month"),

            func.sum(
                Payment.amount
            ).label("revenue")

        )
        .filter(
            Payment.payment_status == "Success"
        )
        .group_by(
            func.date_trunc(
                "month",
                Payment.payment_date
            )
        )
        .order_by(
            func.date_trunc(
                "month",
                Payment.payment_date
            )
        )
        .all()
    )

    return [

        {
            "month":
                str(row.month.date()),

            "revenue":
                float(row.revenue)
        }

        for row in results
    ]

# DESTINATION WISE REVENUE --------------------------------------------------

def destination_wise_revenue(
    db
):

    results = (

        db.query(

            Destination.name,

            func.sum(
                Payment.amount
            ).label("revenue")

        )

        .join(
            TourPackage,
            TourPackage.destination_id ==
            Destination.id
        )

        .join(
            Booking,
            Booking.package_id ==
            TourPackage.id
        )

        .join(
            Payment,
            Payment.booking_id ==
            Booking.id
        )

        .filter(
            Payment.payment_status == "Success"
        )

        .group_by(
            Destination.id,
            Destination.name
        )

        .order_by(
            func.sum(
                Payment.amount
            ).desc()
        )

        .all()
    )

    return [

        {
            "destination": row.name,

            "revenue":
                float(row.revenue)
        }

        for row in results
    ]

# PACKAGE PERFORMANCE REPORT ----------------------------------------------------

def package_performance(
    db
):

    results = (

        db.query(

            TourPackage.package_name,

            func.count(
                Booking.id
            ).label(
                "total_bookings"
            ),

            func.coalesce(

                func.sum(
                    Payment.amount
                ),

                0

            ).label(
                "total_revenue"
            ),

            func.coalesce(

                func.avg(
                    Review.rating
                ),

                0

            ).label(
                "average_rating"
            )

        )

        .outerjoin(

            Booking,

            Booking.package_id ==
            TourPackage.id

        )

        .outerjoin(

            Payment,

            Payment.booking_id ==
            Booking.id

        )

        .outerjoin(

            Review,

            Review.package_id ==
            TourPackage.id

        )

        .filter(

            (Payment.payment_status == "Success")
            |
            (Payment.id == None)

        )

        .group_by(

            TourPackage.id,
            TourPackage.package_name

        )

        .all()
    )

    return [

        {

            "package_name":
                row.package_name,

            "total_bookings":
                row.total_bookings,

            "total_revenue":
                float(
                    row.total_revenue
                ),

            "average_rating":
                round(
                    float(
                        row.average_rating
                    ),
                    2
                )

        }

        for row in results
    ]

# CANCELLATION REPORT ----------------------------------------------------------

def cancellation_report(
    db
):

    results = (

        db.query(

            func.date(
                Booking.booking_date
            ).label(
                "date"
            ),

            func.count(
                Booking.id
            ).label(
                "cancelled_bookings"
            )

        )

        .filter(

            Booking.status ==
            "Cancelled"

        )

        .group_by(

            func.date(
                Booking.booking_date
            )

        )

        .order_by(

            func.date(
                Booking.booking_date
            )

        )

        .all()
    )

    return [

        {

            "date":
                str(row.date),

            "cancelled_bookings":
                row.cancelled_bookings

        }

        for row in results
    ]

# CUSTOMER BOOKING HISTORY -------------------------------------------------

def get_customer_booking_history(
    db,
    customer_id: int
):

    bookings = (

        db.query(Booking)

        .filter(

            Booking.customer_id ==
            customer_id

        )

        .order_by(

            Booking.booking_date.desc()

        )

        .all()
    )

    return bookings
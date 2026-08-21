from sqlalchemy.orm import Session
from sqlalchemy import func

from models.customer_model import Customer
from models.package_model import TourPackage
from models.booking_model import Booking
from models.payment_model import Payment
from models.destination_model import Destination
from models.review_model import Review
from models.cancellation_model import Cancellation


# TOTAL CUSTOMERS -----------------------------------------------------------

def get_total_customers(db: Session):

    return db.query(
        func.count(Customer.id)
    ).scalar()

# TOTAL PACKAGES -----------------------------------------------------------

def get_total_packages(db: Session):

    return db.query(
        func.count(TourPackage.id)
    ).scalar()

# ACTIVE TOURS -----------------------------------------------------------

def get_active_tours(db: Session):

    return db.query(
        func.count(TourPackage.id)
    ).filter(
        TourPackage.status == "Active"
    ).scalar()

# TOTAL BOOKINGS -------------------------------------------------------

def get_total_bookings(db: Session):

    return db.query(
        func.count(Booking.id)
    ).scalar()

# CONFIRMED BOOKINGS --------------------------------------------------

def get_confirmed_bookings(db: Session):

    return db.query(
        func.count(Booking.id)
    ).filter(
        Booking.status == "Confirmed"
    ).scalar()

# CANCELLED BOOKINGS -------------------------------------------------

def get_cancelled_bookings(db: Session):

    return db.query(
        func.count(Booking.id)
    ).filter(
        Booking.status == "Cancelled"
    ).scalar()

# TOTAL REVENUE ----------------------------------------------------

def get_total_revenue(db: Session):

    return db.query(
        func.coalesce(
            func.sum(Payment.amount),
            0
        )
    ).filter(
        Payment.payment_status == "Success"
    ).scalar()

# TOTAL REFUNDS ----------------------------------------------------------

def get_total_refunds(db: Session):

    return db.query(
        func.coalesce(
            func.sum(Cancellation.refund_amount),
            0
        )
    ).scalar()

# MOST POPULAR DESTINATION ------------------------------------------------

def get_popular_destinations(
    db: Session
):

    results = (
        db.query(
            Destination.name,
            func.count(Booking.id)
            .label("total_bookings")
        )
        .join(
            TourPackage,
            TourPackage.destination_id == Destination.id
        )
        .join(
            Booking,
            Booking.package_id == TourPackage.id
        )
        .group_by(
            Destination.id,
            Destination.name
        )
        .order_by(
            func.count(Booking.id).desc()
        )
        .limit(5)
        .all()
    )

    return [
        {
            "destination": row.name,
            "total_bookings": row.total_bookings
        }
        for row in results
    ]

# MOST BOOKED PACKAGES ------------------------------------------------------

def get_most_booked_packages(
    db: Session
):

    results = (
        db.query(
            TourPackage.package_name,
            func.count(Booking.id)
            .label("total_bookings")
        )
        .join(
            Booking,
            Booking.package_id == TourPackage.id
        )
        .group_by(
            TourPackage.id,
            TourPackage.package_name
        )
        .order_by(
            func.count(Booking.id).desc()
        )
        .limit(5)
        .all()
    )

    return [
        {
            "package_name": row.package_name,
            "total_bookings": row.total_bookings
        }
        for row in results
    ]

# PACKAGE RATING ----------------------------------------------------------------

def get_average_package_rating(
    db: Session
):

    return db.query(
        func.coalesce(
            func.avg(Review.rating),
            0
        )
    ).scalar()

def get_package_ratings(
    db: Session
):

    results = (
        db.query(
            TourPackage.package_name,

            func.avg(Review.rating)
            .label("average_rating")
        )
        .outerjoin(
            Review,
            Review.package_id == TourPackage.id
        )
        .group_by(
            TourPackage.id,
            TourPackage.package_name
        )
        .all()
    )

    return [
        {
            "package_name": row.package_name,

            "average_rating": round(
                float(row.average_rating or 0),
                2
            )
        }

        for row in results
    ]

def get_dashboard_data(db: Session):

    total_customers = get_total_customers(db)

    total_packages = get_total_packages(db)

    active_tours = get_active_tours(db)

    total_bookings = get_total_bookings(db)

    confirmed_bookings = get_confirmed_bookings(db)

    cancelled_bookings = get_cancelled_bookings(db)

    total_revenue = get_total_revenue(db)

    total_refunds = get_total_refunds(db)

    average_rating = get_average_package_rating(db)

    popular_destinations = (
        get_popular_destinations(db)
    )

    most_booked_packages = (
        get_most_booked_packages(db)
    )

    return {

        "total_customers":
            total_customers,

        "total_packages":
            total_packages,

        "active_tours":
            active_tours,

        "total_bookings":
            total_bookings,

        "confirmed_bookings":
            confirmed_bookings,

        "cancelled_bookings":
            cancelled_bookings,

        "total_revenue":
            float(total_revenue),

        "total_refunds":
            float(total_refunds),

        "average_package_rating":
            round(
                float(average_rating),
                2
            ),

        "most_popular_destinations":
            popular_destinations,

        "most_booked_packages":
            most_booked_packages
    }


def get_total_refunds(db: Session):

    return db.query(
        func.coalesce(
            func.sum(Cancellation.refund_amount),
            0
        )
    ).scalar()
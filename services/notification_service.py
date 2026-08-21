from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.notification_model import Notification

from repositories import notification_repository

from utils.email import send_email



def send_notification(
    db,
    customer_id,
    customer_email,
    notification_type,
    subject,
    message
):

    # Save notification in database

    notification = Notification(

        customer_id=customer_id,

        notification_type=notification_type,

        subject=subject,

        message=message,

        status="Pending"
    )

    notification = (
        notification_repository
        .create_notification(
            db,
            notification
        )
    )

    # Send email

    try:

        send_email(
            email=customer_email,
            subject=subject,
            message=message
        )

        notification.status = "Sent"

        db.commit()

    except Exception:

        notification.status = "Failed"

        db.commit()

    return notification

def send_booking_confirmation(
    db,
    customer_id,
    customer_email,
    booking_id,
    package_name
):

    return send_notification(

        db=db,

        customer_id=customer_id,

        customer_email=customer_email,

        notification_type="Booking Confirmation",

        subject="Booking Confirmed",

        message=(
            f"Your booking #{booking_id} "
            f"for {package_name} has been confirmed."
        )
    )

def send_payment_success(
    db,
    customer_id,
    customer_email,
    payment_id,
    amount
):

    return send_notification(

        db=db,

        customer_id=customer_id,

        customer_email=customer_email,

        notification_type="Payment Success",

        subject="Payment Successful",

        message=(
            f"Payment #{payment_id} "
            f"of ₹{amount} was successful."
        )
    )

def send_payment_failure(
    db,
    customer_id,
    customer_email,
    payment_id
):

    return send_notification(

        db=db,

        customer_id=customer_id,

        customer_email=customer_email,

        notification_type="Payment Failure",

        subject="Payment Failed",

        message=(
            f"Payment #{payment_id} failed. "
            f"Please try again."
        )
    )

def send_tour_cancellation(
    db,
    customer_id,
    customer_email,
    booking_id,
    reason
):

    return send_notification(

        db=db,

        customer_id=customer_id,

        customer_email=customer_email,

        notification_type="Tour Cancellation",

        subject="Tour Cancelled",

        message=(
            f"Your booking #{booking_id} "
            f"has been cancelled. "
            f"Reason: {reason}"
        )
    )

def send_refund_notification(
    db,
    customer_id,
    customer_email,
    booking_id,
    refund_amount
):

    return send_notification(

        db=db,

        customer_id=customer_id,

        customer_email=customer_email,

        notification_type="Refund",

        subject="Refund Processing",

        message=(
            f"Refund of ₹{refund_amount} "
            f"for booking #{booking_id} "
            f"is being processed."
        )
    )

def send_tour_reminder(
    db,
    customer_id,
    customer_email,
    booking_id,
    package_name,
    tour_date
):

    return send_notification(

        db=db,

        customer_id=customer_id,

        customer_email=customer_email,

        notification_type="Tour Reminder",

        subject="Upcoming Tour Reminder",

        message=(
            f"Reminder: Your {package_name} tour "
            f"is scheduled for {tour_date}."
        )
    )

def send_hotel_confirmation(
    db,
    customer_id,
    customer_email,
    hotel_name,
    booking_id
):

    return send_notification(

        db=db,

        customer_id=customer_id,

        customer_email=customer_email,

        notification_type="Hotel Reservation",

        subject="Hotel Reservation Confirmed",

        message=(
            f"Your hotel reservation at "
            f"{hotel_name} for booking "
            f"#{booking_id} is confirmed."
        )
    )
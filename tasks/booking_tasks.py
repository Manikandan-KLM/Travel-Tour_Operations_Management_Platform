from tasks.celery_app import (
    celery_app
)


@celery_app.task
def send_tour_reminder(
    booking_id: int
):

    print(
        f"Reminder sent for booking {booking_id}"
    )
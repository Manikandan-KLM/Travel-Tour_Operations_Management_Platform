from io import BytesIO

from openpyxl import Workbook


def generate_booking_report(
    bookings
):

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Bookings"

    sheet.append(
        [
            "Booking ID",
            "Customer ID",
            "Package ID",
            "Status"
        ]
    )

    for booking in bookings:

        sheet.append(
            [
                booking.id,
                booking.customer_id,
                booking.package_id,
                booking.status
            ]
        )

    buffer = BytesIO()

    workbook.save(buffer)

    buffer.seek(0)

    return buffer
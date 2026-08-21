from io import BytesIO

from reportlab.pdfgen import canvas


def generate_booking_pdf(
    booking
):

    buffer = BytesIO()

    pdf = canvas.Canvas(
        buffer
    )

    pdf.drawString(
        100,
        750,
        "Travel Booking Confirmation"
    )

    pdf.drawString(
        100,
        700,
        f"Booking ID: {booking.id}"
    )

    pdf.drawString(
        100,
        670,
        f"Status: {booking.status}"
    )

    pdf.save()

    buffer.seek(0)

    return buffer
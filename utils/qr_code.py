import qrcode

from io import BytesIO


def generate_booking_qr(
    booking_id: int
):

    data = (
        f"BOOKING_ID:{booking_id}"
    )

    qr = qrcode.make(data)

    buffer = BytesIO()

    qr.save(
        buffer,
        format="PNG"
    )

    buffer.seek(0)

    return buffer
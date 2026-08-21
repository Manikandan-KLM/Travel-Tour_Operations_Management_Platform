from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey
)

from database import Base


class Cancellation(Base):

    __tablename__ = "cancellations"

    id = Column(Integer,primary_key=True,index=True)

    booking_id = Column(Integer,ForeignKey("bookings.id"),nullable=False)

    cancellation_reason = Column(String,nullable=False)

    cancellation_date = Column(DateTime,nullable=False)

    refund_percentage = Column(Float,nullable=False)

    refund_amount = Column(Float,nullable=False)
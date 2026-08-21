from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.sql import func

from database import Base


class Review(Base):

    __tablename__ = "reviews"

    id = Column(Integer,primary_key=True,index=True)

    customer_id = Column(Integer,ForeignKey("customers.id"),nullable=False)

    package_id = Column(Integer,ForeignKey("packages.id"),nullable=False)

    booking_id = Column(Integer,ForeignKey("bookings.id"),nullable=False)

    rating = Column(Integer,nullable=False)

    review_text = Column(Text,nullable=False)

    created_at = Column(DateTime,server_default=func.now(),nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "booking_id",
            name="uq_review_booking"
        ),
    )
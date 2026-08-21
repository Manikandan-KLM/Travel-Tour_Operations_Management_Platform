from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey
)

from database import Base


class Payment(Base):

    __tablename__ = "payments"

    id = Column(Integer,primary_key=True,index=True)

    booking_id = Column(Integer,ForeignKey("bookings.id"),nullable=False)

    amount = Column(Float,nullable=False)

    payment_method = Column(String,nullable=False)

    transaction_id = Column(String,unique=True,nullable=False,index=True)

    payment_status = Column(String,default="Pending",nullable=False)

    payment_date = Column(DateTime,nullable=False)
from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    String
)

from database import Base


class Traveler(Base):
    __tablename__ = "travelers"

    id = Column(Integer,primary_key=True,index=True)

    booking_id = Column(Integer,ForeignKey("bookings.id"),nullable=False,index=True)

    full_name = Column(String(150),nullable=False)

    date_of_birth = Column(Date,nullable=False)

    gender = Column(String(20),nullable=False)

    passport_number = Column(String(50),nullable=True,index=True)

    nationality = Column(String(100),nullable=False)

    special_requirements = Column(String(500),nullable=True)
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey
)

from database import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer,primary_key=True,index=True)

    hotel_id = Column(Integer,ForeignKey("hotels.id"),nullable=False,index=True)

    room_type = Column(String(50),nullable=False)

    room_number = Column(String(30),nullable=False,index=True)

    price_per_night = Column(Float,nullable=False)

    capacity = Column(Integer,nullable=False)

    availability_status = Column(String(30),nullable=False,default="Available")
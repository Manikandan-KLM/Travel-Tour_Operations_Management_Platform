from sqlalchemy import Column, Integer, String, Float, ForeignKey

from database import Base


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer,primary_key=True,index=True)

    hotel_name = Column(String(150),nullable=False)

    destination_id = Column(Integer,ForeignKey("destinations.id"),nullable=False,index=True)

    address = Column(String(300),nullable=False)

    rating = Column(Float,nullable=False,default=0)

    contact_number = Column(String(20),nullable=False)
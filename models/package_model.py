from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Text

from database import Base


class TourPackage(Base):
    __tablename__ = "packages"

    id = Column(Integer,primary_key=True,index=True)

    package_name = Column(String(150),nullable=False,index=True)

    destination_id = Column(Integer,ForeignKey("destinations.id"),nullable=False,index=True)

    description = Column(Text,nullable=True)

    duration_days = Column(Integer,nullable=False)

    base_price = Column(Float,nullable=False)

    max_capacity = Column(Integer,nullable=False)

    available_slots = Column(Integer,nullable=False)

    start_date = Column(Date,nullable=False)

    end_date = Column(Date,nullable=False)

    status = Column(String(20),nullable=False,default="Draft",index=True)
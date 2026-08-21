from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    Time
)

from database import Base


class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(Integer,primary_key=True,index=True)

    package_id = Column(Integer,ForeignKey("packages.id"),nullable=False,index=True)

    day_number = Column(Integer,nullable=False)

    title = Column(String(150),nullable=False)

    description = Column(Text,nullable=True)

    location = Column(String(150),nullable=False)

    start_time = Column(Time,nullable=False)

    end_time = Column(Time,nullable=False)
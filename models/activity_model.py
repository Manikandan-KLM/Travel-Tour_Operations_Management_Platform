from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship

from database import Base


class Activity(Base):

    __tablename__ = "activities"

    id = Column(Integer,primary_key=True,index=True)

    package_id = Column(Integer,ForeignKey("packages.id"),nullable=False)

    activity_name = Column(String,nullable=False)

    location = Column(String,nullable=False)

    duration = Column(Integer,nullable=False)

    price = Column(Float,nullable=False)

    capacity = Column(Integer,nullable=False)

    start_time = Column(DateTime,nullable=False)

    end_time = Column(DateTime,nullable=False)

    guide_id = Column(Integer,ForeignKey("guides.id"),nullable=True)

    package = relationship("Package")

    guide = relationship("Guide")
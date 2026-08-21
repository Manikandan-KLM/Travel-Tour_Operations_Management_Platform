from sqlalchemy import Column, Integer, String, Text

from database import Base


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer,primary_key=True,index=True)

    name = Column(String(100),nullable=False,index=True)

    country = Column(String(100),nullable=False,index=True)

    state = Column(String(100),nullable=False)

    description = Column(Text,nullable=True)

    best_season = Column(String(50),nullable=False,index=True)

    status = Column(String(20),nullable=False,default="Active",index=True)
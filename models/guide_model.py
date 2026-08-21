from sqlalchemy import Column, Integer, String

from database import Base


class Guide(Base):

    __tablename__ = "guides"

    id = Column(Integer,primary_key=True,index=True)

    name = Column(String,nullable=False)

    email = Column(String,unique=True,nullable=False)

    phone = Column(String,nullable=False)

    specialization = Column(String,nullable=False)

    availability_status = Column(String,default="Active",nullable=False)
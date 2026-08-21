from sqlalchemy import Column, Integer, String

from database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer,primary_key=True,index=True)

    name = Column(String(150),nullable=False)

    email = Column(String(150),nullable=False,unique=True,index=True)

    phone = Column(String(20),nullable=False)

    address = Column(String(300),nullable=True)

    emergency_contact = Column(String(20),nullable=True)
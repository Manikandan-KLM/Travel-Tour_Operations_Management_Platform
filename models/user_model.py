from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from database import Base


class UserRole(str, Enum):
    SUPER_ADMIN = "Super Admin"
    TOUR_MANAGER = "Tour Manager"
    BOOKING_AGENT = "Booking Agent"
    CUSTOMER = "Customer"
    TOUR_GUIDE = "Tour Guide"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password = Column(String(255), nullable=False)

    role = Column(
        String(50),
        nullable=False,
        default=UserRole.CUSTOMER.value
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )
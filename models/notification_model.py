from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from database import Base


class Notification(Base):

    __tablename__ = "notifications"

    id = Column(Integer,primary_key=True,index=True)

    customer_id = Column(Integer,ForeignKey("customers.id"),nullable=False)

    notification_type = Column(String,nullable=False)

    subject = Column(String,nullable=False)

    message = Column(Text,nullable=False)

    status = Column(String,default="Pending",nullable=False)

    created_at = Column(DateTime,server_default=func.now(),nullable=False)
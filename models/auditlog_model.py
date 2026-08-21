from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    JSON
)

from sqlalchemy.sql import func

from database import Base


class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(Integer,primary_key=True)

    user_id = Column(Integer,nullable=True)

    action = Column(String,nullable=False)

    entity = Column(String,nullable=False)

    entity_id = Column(Integer,nullable=True)

    old_data = Column(JSON,nullable=True)

    new_data = Column(JSON,nullable=True)

    created_at = Column(DateTime,server_default=func.now())
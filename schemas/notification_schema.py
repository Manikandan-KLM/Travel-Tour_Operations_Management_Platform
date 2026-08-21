from datetime import datetime

from pydantic import BaseModel


class NotificationResponse(BaseModel):

    id: int

    customer_id: int

    notification_type: str

    subject: str

    message: str

    status: str

    created_at: datetime

    class Config:
        from_attributes = True
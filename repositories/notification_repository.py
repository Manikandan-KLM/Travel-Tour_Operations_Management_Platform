from sqlalchemy.orm import Session

from models.notification_model import Notification


def create_notification(
    db: Session,
    notification: Notification
):

    db.add(notification)

    db.commit()

    db.refresh(notification)

    return notification


def get_customer_notifications(
    db: Session,
    customer_id: int
):

    return db.query(Notification).filter(
        Notification.customer_id == customer_id
    ).order_by(
        Notification.created_at.desc()
    ).all()
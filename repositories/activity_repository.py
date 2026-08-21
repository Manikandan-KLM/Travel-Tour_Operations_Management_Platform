from sqlalchemy.orm import Session

from models.activity_model import Activity

class ActivityRepository:
  
  def create_activity(
    db: Session,
    activity: Activity
):

    db.add(activity)

    db.commit()

    db.refresh(activity)

    return activity


def get_all_activities(
    db: Session
):

    return db.query(Activity).all()


def get_activity_by_id(
    db: Session,
    activity_id: int
):

    return db.query(Activity).filter(
        Activity.id == activity_id
    ).first()


def get_activity_by_package(
    db: Session,
    package_id: int
):

    return db.query(Activity).filter(
        Activity.package_id == package_id
    ).first()


def get_overlapping_activity(
    db: Session,
    guide_id: int,
    start_time,
    end_time,
    activity_id: int
):

    return db.query(Activity).filter(

        Activity.guide_id == guide_id,

        Activity.id != activity_id,

        Activity.start_time < end_time,

        Activity.end_time > start_time

    ).first()


def update_activity(
    db: Session,
    activity: Activity
):

    db.commit()

    db.refresh(activity)

    return activity

activity_repository = ActivityRepository()
from sqlalchemy.orm import Session

from models.guide_model import Guide

class GuideRepository:

 def create_guide(
    db: Session,
    guide: Guide
):

    db.add(guide)

    db.commit()

    db.refresh(guide)

    return guide


def get_all_guides(
    db: Session
):

    return db.query(Guide).all()


def get_guide_by_id(
    db: Session,
    guide_id: int
):

    return db.query(Guide).filter(
        Guide.id == guide_id
    ).first()


def get_guide_by_email(
    db: Session,
    email: str
):

    return db.query(Guide).filter(
        Guide.email == email
    ).first()

guide_repository = GuideRepository()
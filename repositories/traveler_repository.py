from sqlalchemy.orm import Session

from models.traveler_model import Traveler


class TravelerRepository:

    def create(
        self,
        db: Session,
        traveler: Traveler
    ):

        db.add(traveler)
        db.commit()
        db.refresh(traveler)

        return traveler

    def get_by_id(
        self,
        db: Session,
        traveler_id: int
    ):

        return (
            db.query(Traveler)
            .filter(
                Traveler.id == traveler_id
            )
            .first()
        )

    def get_by_booking(
        self,
        db: Session,
        booking_id: int
    ):

        return (
            db.query(Traveler)
            .filter(
                Traveler.booking_id == booking_id
            )
            .order_by(
                Traveler.id.asc()
            )
            .all()
        )

    def update(
        self,
        db: Session,
        traveler: Traveler
    ):

        db.commit()
        db.refresh(traveler)

        return traveler


traveler_repository = TravelerRepository()
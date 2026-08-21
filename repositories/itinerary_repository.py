from sqlalchemy.orm import Session

from models.itinerary_model import Itinerary


class ItineraryRepository:

    def create(
        self,
        db: Session,
        itinerary: Itinerary
    ):

        db.add(itinerary)

        db.commit()

        db.refresh(itinerary)

        return itinerary

    def get_by_id(
        self,
        db: Session,
        itinerary_id: int
    ):

        return (
            db.query(Itinerary)
            .filter(
                Itinerary.id == itinerary_id
            )
            .first()
        )

    def get_by_package_and_day(
        self,
        db: Session,
        package_id: int,
        day_number: int
    ):

        return (
            db.query(Itinerary)
            .filter(
                Itinerary.package_id == package_id,
                Itinerary.day_number == day_number
            )
            .first()
        )

    def get_by_package(
        self,
        db: Session,
        package_id: int
    ):

        return (
            db.query(Itinerary)
            .filter(
                Itinerary.package_id == package_id
            )
            .order_by(
                Itinerary.day_number.asc()
            )
            .all()
        )

    def update(
        self,
        db: Session,
        itinerary: Itinerary
    ):

        db.commit()

        db.refresh(itinerary)

        return itinerary

    def delete(
        self,
        db: Session,
        itinerary: Itinerary
    ):

        db.delete(itinerary)

        db.commit()


itinerary_repository = ItineraryRepository()
from sqlalchemy.orm import Session

from models.hotel_model import Hotel


class HotelRepository:

    def create(
        self,
        db: Session,
        hotel: Hotel
    ):

        db.add(hotel)
        db.commit()
        db.refresh(hotel)

        return hotel

    def get_by_id(
        self,
        db: Session,
        hotel_id: int
    ):

        return (
            db.query(Hotel)
            .filter(
                Hotel.id == hotel_id
            )
            .first()
        )

    def get_all(
        self,
        db: Session
    ):

        return (
            db.query(Hotel)
            .order_by(
                Hotel.id.desc()
            )
            .all()
        )


hotel_repository = HotelRepository()